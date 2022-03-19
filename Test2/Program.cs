// See https://aka.ms/new-console-template for more information
using System.Reflection;
using SkiaSharp;
// See https://aka.ms/new-console-template for more information
using MaterialColorUtilities.Utils;

using MaterialColorUtilities.Palettes;
using MaterialColorUtilities.Schemes;

using System.Drawing;
using System.Text;
using Newtonsoft.Json;
using System.Text.RegularExpressions;
// --- Console.WriteLine("Hello, World!");

class Program
{
    // Generate seed color from an image:
    // Load the image into an int[].
    // The image is stored in an embedded resource, and then decoded and resized using SkiaSharp.
    static string imageResourceId = "Test2.Resources.wallpaper.png";
    static Stream resourceStream = Assembly.GetExecutingAssembly().GetManifestResourceStream(imageResourceId)!;
    static SKBitmap bitmap = SKBitmap.Decode(resourceStream).Resize(new SKImageInfo(112, 112), SKFilterQuality.Medium);
    static int[] pixels = bitmap.Pixels.Select(p => (int)(uint)p).ToArray();

    // This is where the magic happens
    static int seedColor = ImageUtils.ColorFromImage(pixels);

    // CorePalette gives you access to every tone of the key colors
    static CorePalette corePalette = CorePalette.Of(seedColor);

    // override some colors of the Light scheme ;)
    class MyLightScheme : LightScheme
    {

        public MyLightScheme(CorePalette corePalette) : base(corePalette) { }
        //string s = "String from MyScheme";

        protected override int BackgroundLight => corePalette.Neutral[99];
    }

    // override some colors of the Light scheme ;)
    class MyDarkScheme : DarkScheme
    {

        public MyDarkScheme(CorePalette corePalette) : base(corePalette) { }
        //string s = "String from MyScheme";

        protected override int BackgroundDark => corePalette.Primary[1000];
    }

    // Main Method
    static void Main()
    {
        // Create custom schemes
        MyLightScheme lightScheme = new(corePalette);
        MyDarkScheme darkScheme = new(corePalette);

        // Save color palette for export
        var colors = new Dictionary<string, string>();

        // light section of export
        var colors_light = new Dictionary<string, string>();
        foreach (var property in typeof(Scheme<int>).GetProperties())
        {
            int color = (int)property.GetValue(lightScheme)!;
            //Console.WriteLine($"{property.Name}: #{color.ToString("X")[2..]}");
            colors_light.Add(property.Name, "#" + color.ToString("X")[2..]);
        }

        // dark section of export
        var colors_dark = new Dictionary<string, string>();
        foreach (var property in typeof(Scheme<int>).GetProperties())
        {
            int color = (int)property.GetValue(darkScheme)!;
            //Console.WriteLine($"{property.Name}: #{color.ToString("X")[2..]}");
            colors_dark.Add(property.Name, "#" + color.ToString("X")[2..]);
        }

        // light to json
        string jsonLight = JsonConvert.SerializeObject(colors_light);
        //string jsonLightUnescaped = Regex.Unescape(jsonLight);
        //colors.Add("light", jsonLightUnescaped);

        // dark to json
        string jsonDark = JsonConvert.SerializeObject(colors_dark);
        // string jsonDarkUnescaped = Regex.Unescape(jsonDark);
        // colors.Add("dark", jsonDarkUnescaped);

        //string jsonString = JsonConvert.SerializeObject(colors_light);

        //jsonString = Regex.Unescape(jsonString);
        //Console.WriteLine(jsonString);
        Console.Write("{\"light\":");
        Console.WriteLine(jsonLight+",");
        Console.WriteLine("\"dark\":");
        Console.WriteLine(jsonDark);
        Console.WriteLine("}");

    }
}
