using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Data.Core;
using Avalonia.Data.Core.Plugins;
using System;
using System.Linq;
using Avalonia.Input;
using Avalonia.Markup.Xaml;
using RandPicker.ViewModels;
using RandPicker.Views;
using System.Windows.Input;
using CommunityToolkit.Mvvm.Input;
using Serilog;

namespace RandPicker;

public partial class App : Application
{
    public static ICommand ExitComm { get; } = new RelayCommand(Exit);
    public static ICommand StuSetCom { get; } = new RelayCommand(StudentSettings);
    public static ICommand GroupSetCom { get; } = new RelayCommand(GroupSettings);
    public static ICommand UiSetCom { get; } = new RelayCommand(UiSettings);

    private static SettingsWindow? _settingsWindow;

    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            // Avoid duplicate validations from both Avalonia and the CommunityToolkit. 
            // More info: https://docs.avaloniaui.net/docs/guides/development-guides/data-validation#manage-validationplugins
            DisableAvaloniaDataAnnotationValidation();
            desktop.MainWindow = new MainWindow
            {
                DataContext = new MainWindowViewModel(),
            };
        }

        base.OnFrameworkInitializationCompleted();
    }

    private void DisableAvaloniaDataAnnotationValidation()
    {
        // Get an array of plugins to remove
        var dataValidationPluginsToRemove =
            BindingPlugins.DataValidators.OfType<DataAnnotationsValidationPlugin>().ToArray();

        // remove each entry found
        foreach (var plugin in dataValidationPluginsToRemove)
        {
            BindingPlugins.DataValidators.Remove(plugin);
        }
    }

    private static void Exit()
    {
        if (Current?.ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            desktop.Shutdown();
        }
    }
    
    private static void StudentSettings()
    {
        Settings();
        if (_settingsWindow != null)
        {
            _settingsWindow.Turn2Page(0);
            return;
        }
        Log.Error("打开学生设置失败。");
    }

    private static void GroupSettings()
    {
        Settings();
        if (_settingsWindow != null)
        {
            _settingsWindow.Turn2Page(1);
            return;
        }
        Log.Error("打开小组设置失败。");
    }

    private static void UiSettings()
    {
        Settings();
        if (_settingsWindow != null)
        {
            _settingsWindow.Turn2Page(2);
            return;
        }
        Log.Error("打开界面设置失败。");
    }

    private static void Settings()
    {
        Log.Debug("打开设置。");
        // 设置防多开
        if (_settingsWindow != null)
        {
            _settingsWindow.Activate();
            _settingsWindow.Focus();
            Log.Debug("已存在设置窗口。");
            return;
        }
        _settingsWindow = new SettingsWindow();
        _settingsWindow.Closed += (_, _) => _settingsWindow = null;
        _settingsWindow.Show();
        Log.Debug("打开新的设置窗口。");
    }
}