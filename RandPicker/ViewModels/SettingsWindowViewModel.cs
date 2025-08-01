using System.Collections.ObjectModel;

namespace RandPicker.ViewModels;

public class SettingsWindowViewModel : ViewModelBase
{
    public class SettingsItem
    {
        public string Title { get; set; } = "关于";
        public string Icon { get; set; } = "About";
    }
    
    public ObservableCollection<SettingsItem> SettingsItems { get; } = new ObservableCollection<SettingsItem>
    {
        new SettingsItem { Title = "通用设置", Icon = "Settings" },
        new SettingsItem { Title = "主题设置", Icon = "" }
    };
}