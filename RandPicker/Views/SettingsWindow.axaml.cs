using System;
using System.Collections.ObjectModel;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using Serilog;

namespace RandPicker.Views;

public partial class SettingsWindow : Window
{
    public SettingsWindow()
    {
        InitializeComponent(); 
        DataContext = new ViewModels.SettingsWindowViewModel();

        NavList.PointerReleased += OnSelectionChanged;
    }

    

    public void OnSelectionChanged(object? sender, RoutedEventArgs? args)
    {
        if (sender is not ListBox listBox)
            return;

        if (!listBox.IsFocused && !listBox.IsKeyboardFocusWithin)
            return;
        try
        {
            PageCarousel.SelectedIndex = listBox.SelectedIndex;
            Scroller.Offset = Vector.Zero;
            Scroller.VerticalScrollBarVisibility =
                ((Control)PageCarousel.SelectedItem!).GetValue(ScrollViewer.VerticalScrollBarVisibilityProperty);
        }
        catch (Exception ex)
        {
            // ignored
            Log.Error("切换设置页面时出错：{ex}", ex.Message);
        }

        NavDrawer.OptionalCloseLeftDrawer();
        NavToggle.IsChecked = false;
    }
}