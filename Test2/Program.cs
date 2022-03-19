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

        protected override int BackgroundLight => corePalette.Primary[1000];
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
        
        MyLightScheme lightScheme = new(corePalette);
        MyDarkScheme darkScheme = new(corePalette);

        // 'E' is object of class stream
        // also works as object of
        // class 'web'
        //MyScheme E = MyScheme;
        //LightSchem<int> scheme = new LightScheme(corePalette);

        foreach (var property in typeof(Scheme<int>).GetProperties())
        {
            // var colors_light = new Dictionary<string, string>();
            int color = (int)property.GetValue(lightScheme)!;
            Console.WriteLine($"{property.Name}: #{color.ToString("X")[2..]}");
            //colors_light.Add(property.Name, "#" + color.ToString("X")[2..]);
        }

        foreach (var property in typeof(Scheme<int>).GetProperties())
        {
            // var colors_light = new Dictionary<string, string>();
            int color = (int)property.GetValue(darkScheme)!;
            Console.WriteLine($"{property.Name}: #{color.ToString("X")[2..]}");
            //colors_light.Add(property.Name, "#" + color.ToString("X")[2..]);
        }

        Console.WriteLine("aa");
        // it first invokes 'showdata()'
        // of class 'web' then it invokes
        // 'showdata()' of class 'stream'
        //E.showdata();

    }
}
