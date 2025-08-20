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
        // IMPORTANT: 在这里改完之后看看App.axaml.cs
        new SettingsItem { Title = "通用设置", Icon = "Settings" },
        new SettingsItem { Title = "关于", Icon = "About" } // 关于
    };
}