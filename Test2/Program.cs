// See https://aka.ms/new-console-template for more information
using System.Reflection;
using SkiaSharp;
// See https://aka.ms/new-console-template for more information
using MaterialColorUtilities.Utils;

using MaterialColorUtilities.Palettes;
using MaterialColorUtilities.Schemes;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Drawing;
using System.Text;
using System.Text.RegularExpressions;
// --- Console.WriteLine("Hello, World!");


// Generate seed color from an image:
// Load the image into an int[].
// The image is stored in an embedded resource, and then decoded and resized using SkiaSharp.
string imageResourceId = "Test2.Resources.wallpaper.png";

// --- Console.WriteLine(imageResourceId);

using Stream resourceStream = Assembly.GetExecutingAssembly().GetManifestResourceStream(imageResourceId)!;
SKBitmap bitmap = SKBitmap.Decode(resourceStream).Resize(new SKImageInfo(112, 112), SKFilterQuality.Medium);
int[] pixels = bitmap.Pixels.Select(p => (int)(uint)p).ToArray();

// This is where the magic happens
int seedColor = ImageUtils.ColorFromImage(pixels);
// --- Console.WriteLine(seedColor);

// --- Console.WriteLine($"Seed: #{seedColor.ToString("X")[2..]}");

// CorePalette gives you access to every tone of the key colors
CorePalette corePalette = CorePalette.Of(seedColor);

// --- Console.WriteLine("\n============\nLIGHT\n============");
LightScheme lightScheme = new(corePalette);

//TEst of single color
//Console.WriteLine(lightScheme.OnBackground);

// Create an array of cthe colors
var colors = new Dictionary<string, string>();
var colors_light = new Dictionary<string, string>();
// Iterate on light scheme
foreach (var property in typeof(Scheme<int>).GetProperties())
{
    // var colors_light = new Dictionary<string, string>();
    int color = (int)property.GetValue(lightScheme)!;
    // --- Console.WriteLine($"{property.Name}: #{color.ToString("X")[2..]}");
    colors_light.Add(property.Name,"#"+color.ToString("X")[2..]);
}

// --- Console.WriteLine("\n============\nLIGHT\n============");
DarkScheme darkScheme = new(corePalette);
var colors_dark = new Dictionary<string, string>();
// Iterate on dark scheme
foreach (var property in typeof(Scheme<int>).GetProperties())
{
    // var colors_light = new Dictionary<string, string>();
    int color = (int)property.GetValue(darkScheme)!;
    // --- Console.WriteLine($"{property.Name}: #{color.ToString("X")[2..]}");
    colors_dark.Add(property.Name,"#"+color.ToString("X")[2..]);
}

// light
string jsonLight = JsonSerializer.Serialize(colors_light);
string jsonLightUnescaped = Regex.Unescape(jsonLight);
//colors.Add("light",colors_light);

// dark
string jsonDark = JsonSerializer.Serialize(colors_dark);
string jsonDarkUnescaped = Regex.Unescape(jsonDark);
//colors.Add("dark",jsonDarkUnescaped);


string jsonString = JsonSerializer.Serialize(colors);

jsonString = Regex.Unescape(jsonString);
Console.WriteLine("{\"light\":");
Console.WriteLine(jsonLight+",");
Console.WriteLine("\"dark\":");
Console.WriteLine(jsonDark);
Console.WriteLine("}");


