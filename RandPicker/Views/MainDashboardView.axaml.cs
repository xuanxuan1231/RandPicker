using Avalonia.Controls;
using RandPicker.ViewModels;

namespace RandPicker.Views
{
    public partial class MainDashboardView : UserControl
    {
        public MainDashboardView()
        {
            InitializeComponent();
            DataContext = new MainDashboardViewModel();
        }
    }
}