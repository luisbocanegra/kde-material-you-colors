// See https://aka.ms/new-console-template for more information
using SkiaSharp;
using MaterialColorUtilities.Palettes;
using MaterialColorUtilities.Schemes;
using MaterialColorUtilities.Quantize;
using Newtonsoft.Json;
using MaterialColorUtilities.Utils;
using MaterialColorUtilities.Score;
using CommandLine;

class Options
{
    [Option('i', "image", Required = false,
    HelpText = "Absolute path of image file")]
    public string? image { get; set; }

    [Option('n', "ncolor", Required = false,
    HelpText = "Alternative color (if any) to the default best one")]
    public int? ncolor { get; set; }

    [Option('c', "color", Required = false,
    HelpText = "hex color e.g. '#ff0000', (double or single quoted)")]
    public string? hexColor { get; set; }

}


class Program
{
    //private static  bestColors =  new Dictionary<string, string>();
    public static Dictionary<string, string> bestColors = new Dictionary<string, string>();
    public static int seedNo = 0;

    // Given a image, the alt color  and hex color
    // return a selected color or a single color for hex code
    public static int GetColor(string? path, int altColor, string? hexColor)
    {
        int seedColor = 0;
        List<int> seedColors = new List<int>();
        if (path != null)
        {
            // Open filestream of image as read only
            FileStream fs = File.Open(path, FileMode.Open, FileAccess.Read);
            // Then decode and resize using SkiaSharp.
            SKImage img = SKImage.FromEncodedData(fs);
            SKBitmap bitmap = SKBitmap.FromImage(img).Resize(new SKImageInfo(112, 112), SKFilterQuality.Medium);
            fs.Close();
            int[] pixels = bitmap.Pixels.Select(p => (int)(uint)p).ToArray();

            // This is where the magic happens
            // Get a list from the best colors that will at least contain one element
            seedColors = ImageUtils.ColorsFromImage(pixels);

            foreach (var color in seedColors)
            {
                bestColors.Add((seedColors.IndexOf(color)).ToString(), "#" + color.ToString("X")[2..]);
            }

            int totalColors = seedColors.Count;
            // If the requested index is less or equal than the lenght of the colors list 
            if (totalColors > altColor)
            {
                // get the color from the list
                seedColor = seedColors[altColor];
                seedNo = altColor;

            }
            else
            // if the requested index is larger than the colors index use the last one
            {
                seedColor = seedColors[totalColors - 1];
                seedNo = totalColors - 1;
            }
        }
        else if (hexColor != null)
        {
            // convert hex color to rgb then to int
            int rgb = Convert.ToInt32(hexColor.Replace("#", ""), 16);
            int r = (rgb & 0xff0000) >> 16;
            int g = (rgb & 0xff00) >> 8;
            int b = (rgb & 0xff);

            byte[] brgb = { Convert.ToByte(r), Convert.ToByte(g), Convert.ToByte(b) };

            uint a = ColorUtils.IntFromRgb(brgb);

            seedColor = (int)a;
            bestColors.Add("0", hexColor);
        }
        return seedColor;
    }

    // Main Method
    static void Main(string[] args)
    {

        // Get commandline arguments
        int altColor = 0;
        var options = new Options();
        CommandLine.Parser.Default.ParseArguments<Options>(args)
            .WithParsed<Options>(opts => options = opts);


        // Load the image from passed argument with absolute path
        string? path = options.image;
        // get the alt color argument or default to 0 if not given
        altColor = options.ncolor ?? 0;
        // get hex color from commandline
        string? hexColor = options.hexColor;


        if (options.image != null || options.hexColor != null)
        {
            // Given a image, the alt color  and hex color
            // return a selected color or a single color for hex code
            int seedColor = GetColor(path, altColor, hexColor);

            // CorePalette gives you access to every tone of the key colors
            CorePalette corePalette = CorePalette.Of(seedColor);

            // Map the core palette to color schemes
            // A Scheme contains the named colors, like Primary or OnTertiaryContainer
            Scheme<int> lightScheme = new LightSchemeMapper().Map(corePalette);
            Scheme<int> darkScheme = new DarkSchemeMapper().Map(corePalette);

            //TODO: Save color palette to single json
            // var colors = new Dictionary<string, string>();

            // light section of export


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

            // get all tones of core palettes
            var primaryTones = new Dictionary<string, string>();
            for (int i = 0; i< 100; i++)
            {
                int color = corePalette.Primary[i]!;
                primaryTones.Add(Convert.ToString(i), "#" + color.ToString("X")[2..]);
            }

            var secondaryTones = new Dictionary<string, string>();
            for (int i = 0; i< 100; i++)
            {
                int color = corePalette.Secondary[i]!;
                secondaryTones.Add(Convert.ToString(i), "#" + color.ToString("X")[2..]);
            }

            var tertiaryTones = new Dictionary<string, string>();
            for (int i = 0; i< 100; i++)
            {
                int color = corePalette.Tertiary[i]!;
                tertiaryTones.Add(Convert.ToString(i), "#" + color.ToString("X")[2..]);
            }

            var neutralTones = new Dictionary<string, string>();
            for (int i = 0; i< 100; i++)
            {
                int color = corePalette.Neutral[i]!;
                neutralTones.Add(Convert.ToString(i), "#" + color.ToString("X")[2..]);
            }

            var neutralVariantTones = new Dictionary<string, string>();
            for (int i = 0; i< 100; i++)
            {
                int color = corePalette.Neutral[i]!;
                neutralVariantTones.Add(Convert.ToString(i), "#" + color.ToString("X")[2..]);
            }

            string jsonPrimaryTones = JsonConvert.SerializeObject(primaryTones);
            string jsonSecondaryTones = JsonConvert.SerializeObject(secondaryTones);
            string jsonTertiaryTones = JsonConvert.SerializeObject(tertiaryTones);
            string jsonNeutraTones = JsonConvert.SerializeObject(neutralTones);
            string jsonNeutralVariantTones = JsonConvert.SerializeObject(neutralVariantTones);

            string jsonBestColors = JsonConvert.SerializeObject(bestColors);

            // light to json
            string jsonLight = JsonConvert.SerializeObject(colors_light);

            // dark to json
            string jsonDark = JsonConvert.SerializeObject(colors_dark);

            Console.WriteLine("{\"bestColors\":" + jsonBestColors + ",");
            Console.WriteLine("\"seedColor\":{\"" + seedNo + "\":\"#" + seedColor.ToString("X")[2..] + "\"},");
            Console.WriteLine("\"light\":" + jsonLight + ",");
            Console.WriteLine("\"dark\":" + jsonDark + ",");
            Console.WriteLine("\"primaryTones\":" + jsonPrimaryTones + ",");
            Console.WriteLine("\"secondaryTones\":" + jsonSecondaryTones + ",");
            Console.WriteLine("\"tertiaryTones\":" + jsonTertiaryTones + ",");
            Console.WriteLine("\"neutralTones\":" + jsonNeutraTones + ",");
            Console.WriteLine("\"neutralVariantTones\":" + jsonNeutralVariantTones + "}");
        }
    }
}
