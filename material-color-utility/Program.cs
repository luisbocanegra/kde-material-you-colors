// See https://aka.ms/new-console-template for more information
using SkiaSharp;
using MaterialColorUtilities.Palettes;
using MaterialColorUtilities.Schemes;
using MaterialColorUtilities.Quantize;
using Newtonsoft.Json;

class Program
{
    // Return a list of 1+ best colors
    public static List<int> ColorsFromImage(int[] pixels)
    {
        var result = QuantizerCelebi.Quantize(pixels,128);
        var ranked = new List<int>(Custom.Scorer.Score(result));
        //var top = ranked.First();
        return ranked;
    }
    // Main Method
    static void Main(string[] args)
    {
        // Generate seed color from an image
        // Load the image from passed argument with absolute path
        string path = args[0];
        // get the alt color argument or default to 0 if not given
        int altColor = 0;
        if (args.Length > 1)
        {
            altColor = int.Parse(args[1]);
        }
        
        // Open filestream of image as read only
        FileStream fs = File.Open(path, FileMode.Open, FileAccess.Read);

        // Then decode and resize using SkiaSharp.
        SKImage img = SKImage.FromEncodedData(fs);
        SKBitmap bitmap = SKBitmap.FromImage(img).Resize(new SKImageInfo(112, 112), SKFilterQuality.Medium);

        int[] pixels = bitmap.Pixels.Select(p => (int)(uint)p).ToArray();

        // This is where the magic happens
        // Get a list from the best colors that will at least contain one element
        var seedColors = ColorsFromImage(pixels);
        
        int totalColors=seedColors.Count;
        int seedColor,seedNo = 0;
        // If the requested index is less or equal than the lenght of the colors list 
        if (totalColors > altColor)
        {
            // get the color from the list
            seedColor = seedColors[altColor];
            seedNo = altColor;
            
        }else
        // if the requested index is larger than the colors index use the last one
        {
            seedColor = seedColors[totalColors-1];
            seedNo = totalColors-1;
        }

        // CorePalette gives you access to every tone of the key colors
        CorePalette myCorePalette = CorePalette.Of(seedColor);

        // Create custom schemes
        LightScheme lightScheme = new(myCorePalette);
        DarkScheme darkScheme = new(myCorePalette);

        //TODO: Save color palette to single json
        // var colors = new Dictionary<string, string>();

        // light section of export
        var bestColors = new Dictionary<string, string>();
        foreach (var color in seedColors)
        {
            bestColors.Add((seedColors.IndexOf(color)).ToString(), "#" + color.ToString("X")[2..]);
        }

        // light section of export
        var colors_light = new Dictionary<string, string>();
        foreach (var property in typeof(Scheme<int>).GetProperties())
        {
            int color = (int)property.GetValue(lightScheme)!;
            colors_light.Add(property.Name, "#" + color.ToString("X")[2..]);
        }

        // dark section of export
        var colors_dark = new Dictionary<string, string>();
        foreach (var property in typeof(Scheme<int>).GetProperties())
        {
            int color = (int)property.GetValue(darkScheme)!;
            colors_dark.Add(property.Name, "#" + color.ToString("X")[2..]);
        }

        string jsonBestColors = JsonConvert.SerializeObject(bestColors);

        // light to json
        string jsonLight = JsonConvert.SerializeObject(colors_light);

        // dark to json
        string jsonDark = JsonConvert.SerializeObject(colors_dark);

        Console.WriteLine("{\"bestColors\":"+jsonBestColors + ",");
        Console.WriteLine("\"seedColor\":{\""+seedNo+"\":\"#"+seedColor.ToString("X")[2..]+"\"},");
        Console.WriteLine("\"light\":"+jsonLight + ",");
        Console.WriteLine("\"dark\":"+jsonDark+"}");
    }
}
