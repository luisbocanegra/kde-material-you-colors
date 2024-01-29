/*
 * SPDX-FileCopyrightText: 2018 Red Hat Inc
 *
 * SPDX-License-Identifier: LGPL-2.0-or-later
 *
 * SPDX-FileCopyrightText: 2018 Jan Grulich <jgrulich@redhat.com>
 * SPDX-FileCopyrightText: 2024 Luis Bocanegra <luisbocanegra17b@gmail.com>
 */

#include <QByteArray>
#include <QDBusConnection>
#include <QDBusInterface>
#include <QDBusReply>
#include <QDBusUnixFileDescriptor>
#include <QDebug>
#include <QDir>
#include <QFileInfo>
#include <QFuture>
#include <QImage>
#include <poll.h>
#include <qplatformdefs.h>

static int readData(int fd, QByteArray &data) {
    char buffer[4096];
    pollfd pfds[1];
    pfds[0].fd = fd;
    pfds[0].events = POLLIN;

    while (true) {
        // give user 30 sec to click a window, afterwards considered as error
        const int ready = poll(pfds, 1, 30000);
        if (ready < 0) {
            if (errno != EINTR) {
                qWarning() << "poll() failed:" << strerror(errno);
                return -1;
            }
        } else if (ready == 0) {
            qDebug() << "failed to read screenshot: timeout";
            return -1;
        } else if (pfds[0].revents & POLLIN) {
            const int n = QT_READ(fd, buffer, sizeof(buffer));

            if (n < 0) {
                qWarning() << "read() failed:" << strerror(errno);
                return -1;
            } else if (n == 0) {
                return 0;
            } else if (n > 0) {
                data.append(buffer, n);
            }
        } else if (pfds[0].revents & POLLHUP) {
            return 0;
        } else {
            qWarning() << "failed to read screenshot: pipe is broken";
            return -1;
        }
    }

    Q_UNREACHABLE();
}

int saveImage(int pipeFd, QVariantMap imageInfo, QString output_file) {
    QByteArray content;
    if (readData(pipeFd, content) != 0) {
        close(pipeFd);
        return 1;
    }

    close(pipeFd);

    int imageWidth = imageInfo.value("width").toUInt();
    int imageHeight = imageInfo.value("height").toUInt();
    int imageStride = imageInfo.value("stride").toUInt();
    int imageFormat = imageInfo.value("format").toUInt();

    QImage::Format qimageFormat = static_cast<QImage::Format>(imageFormat);
    QImage image = QImage(reinterpret_cast<uchar *>(content.data()), imageWidth,
                          imageHeight, imageStride, qimageFormat);
    image.save(output_file, "PNG", 100);
    return 0;
}

bool isPathWritable(QString path) {
    QFileInfo fileInfo(path);
    QFileInfo parentDirInfo(fileInfo.dir().absolutePath());
    if (!fileInfo.dir().exists()) {
        qWarning("Output location '%s' doesn't exist",
                 qPrintable(fileInfo.dir().absolutePath()));
        return false;
    }
    if (!parentDirInfo.isWritable()) {
        qWarning("Output location '%s' not writable", qPrintable(path));
        return false;
    }
    return true;
}

QString getAbsolutePath(const QString &path) {
    QDir dir(path);
    return dir.absolutePath();
}

QDBusReply<QVariantMap> takeScreenshot(QString window_handle, int pipeFd) {
    // Create a connection to the session bus
    QDBusConnection bus = QDBusConnection::sessionBus();

    // Get a proxy for the KWin object
    QDBusInterface screenshot(QStringLiteral("org.kde.KWin"),
                              QStringLiteral("/org/kde/KWin/ScreenShot2"),
                              QStringLiteral("org.kde.KWin.ScreenShot2"), bus);

    // Options for the screenshot
    QVariantMap options;
    options["include-cursor"] = false;
    options["native-resolution"] = true;
    options["include-shadow"] = false;
    options["include-decoration"] = false;

    // Call CaptureWindow method
    QDBusReply<QVariantMap> reply =
        screenshot.call("CaptureWindow", window_handle, options,
                        QVariant::fromValue(QDBusUnixFileDescriptor(pipeFd)));
    return reply;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        qWarning("Please provide window id and output filename");
        return 1;
    }

    QString window_handle = argv[1];
    QString output_file = argv[2];

    if (output_file.trimmed().isEmpty()) {
        qWarning("Empty filename");
        return 1;
    }

    output_file = getAbsolutePath(output_file);

    if (!isPathWritable(output_file)) {
        return 1;
    }

    int pipeFds[2];
    if (pipe2(pipeFds, O_CLOEXEC | O_NONBLOCK) != 0) {
        qDebug() << "error";
        return 1;
    }

    QDBusReply<QVariantMap> reply = takeScreenshot(window_handle, pipeFds[1]);

    if (!reply.isValid()) {
        qWarning("Failed to capture window %s: %s", qPrintable(window_handle),
                 qPrintable(reply.error().message()));
        return 1;
    }

    ::close(pipeFds[1]);

    QVariantMap imageInfo = reply.value();
    saveImage(pipeFds[0], imageInfo, output_file);
    return 0;
}
