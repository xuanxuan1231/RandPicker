using Avalonia.Controls;
using RandPicker.ViewModels;

namespace RandPicker.Views
{
    public partial class StudentManagementView : UserControl
    {
        public StudentManagementView()
        {
            InitializeComponent();
            DataContext = new StudentManagementViewModel();
        }
    }
}