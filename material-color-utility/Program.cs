// See https://aka.ms/new-console-template for more information
using SkiaSharp;
using MaterialColorUtilities.Utils;
using MaterialColorUtilities.Palettes;
using MaterialColorUtilities.Schemes;
using Newtonsoft.Json;

class Program
{
    // Main Method
    static void Main(string[] args)
    {
        // Generate seed color from an image
    
        // Load the image from passed argument with absolute path
        string path = string.Join('-',args);
        // Open filestream of image as read only
        FileStream fs = File.Open(path, FileMode.Open, FileAccess.Read);

        // Then decode and resize using SkiaSharp.
        SKImage img = SKImage.FromEncodedData(fs);
        SKBitmap bitmap = SKBitmap.FromImage(img).Resize(new SKImageInfo(112, 112), SKFilterQuality.Medium);

        int[] pixels = bitmap.Pixels.Select(p => (int)(uint)p).ToArray();

        // This is where the magic happens
        int seedColor = ImageUtils.ColorFromImage(pixels);

        // CorePalette gives you access to every tone of the key colors
        CorePalette myCorePalette = CorePalette.Of(seedColor);

        // Create custom schemes
        LightScheme lightScheme = new(myCorePalette);
        DarkScheme darkScheme = new(myCorePalette);

        //TODO: Save color palette to single json
        // var colors = new Dictionary<string, string>();

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

        // dark to json
        string jsonDark = JsonConvert.SerializeObject(colors_dark);

        Console.Write("{\"light\":");
        Console.WriteLine(jsonLight + ",");
        Console.WriteLine("\"dark\":");
        Console.WriteLine(jsonDark);
        Console.WriteLine("}");
    }
}
