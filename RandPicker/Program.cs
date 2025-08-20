using Avalonia;
using System;
using System.IO;
using System.Reflection;
using Serilog;

namespace RandPicker;

sealed class Program
{
    // Initialization code. Don't use any Avalonia, third-party APIs or any
    // SynchronizationContext-reliant code before AppMain is called: things aren't initialized
    // yet and stuff might break.
    [STAThread]
    public static void Main(string[] args)
    {
        // 初始化Serilog
        InitializeLogger();


        try
        {
            Log.Information(
                $"RandPicker 启动。版本 v{System.Reflection.Assembly.GetExecutingAssembly().GetName().Version}。");
            // Log.Information(AppDomain.CurrentDomain.BaseDirectory);
            BuildAvaloniaApp().StartWithClassicDesktopLifetime(args);
        }
        catch (Exception ex)
        {
            Log.Fatal(ex, "出现致命错误。");
        }
        finally
        {
            Log.CloseAndFlush();
        }
    }

    // Avalonia configuration, don't remove; also used by visual designer.
    public static AppBuilder BuildAvaloniaApp()
        => AppBuilder.Configure<App>()
            .UsePlatformDetect()
            .WithInterFont()
            .LogToTrace();

    private static void InitializeLogger()
    {
        Log.Logger = new LoggerConfiguration()
            .MinimumLevel.Debug()
            .WriteTo.Console()
            .WriteTo.File("logs/RandPicker.log",
                rollingInterval: RollingInterval.Day,
                retainedFileCountLimit: 7,
                fileSizeLimitBytes: 10 * 1024 * 1024) // 10MB
            .CreateLogger();
    }
}