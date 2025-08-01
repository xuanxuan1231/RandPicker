using Avalonia;
using Avalonia.Controls;
using Avalonia.Markup.Xaml;

namespace RandPicker.Views;

public partial class TestView : UserControl
{
    public TestView()
    {
        AvaloniaXamlLoader.Load(this);
    }
}
