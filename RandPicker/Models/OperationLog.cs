using System;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace RandPicker.Models
{
    /// <summary>
    /// 操作类型枚举
    /// </summary>
    public enum OperationType
    {
        Create,     // 创建
        Update,     // 更新
        Delete,     // 删除
        View,       // 查看
        Export,     // 导出
        Import,     // 导入
        Login,      // 登录
        Logout      // 登出
    }

    /// <summary>
    /// 操作日志模型
    /// </summary>
    public class OperationLog : INotifyPropertyChanged
    {
        private string _id = Guid.NewGuid().ToString();
        private DateTime _timestamp = DateTime.Now;
        private string _userId = string.Empty;
        private string _userName = string.Empty;
        private OperationType _operationType = OperationType.View;
        private string _module = string.Empty;
        private string _description = string.Empty;
        private string _targetId = string.Empty;
        private string _targetName = string.Empty;
        private string _ipAddress = string.Empty;
        private bool _success = true;
        private string _errorMessage = string.Empty;

        public string Id
        {
            get => _id;
            set => SetProperty(ref _id, value);
        }

        public DateTime Timestamp
        {
            get => _timestamp;
            set => SetProperty(ref _timestamp, value);
        }

        public string UserId
        {
            get => _userId;
            set => SetProperty(ref _userId, value);
        }

        public string UserName
        {
            get => _userName;
            set => SetProperty(ref _userName, value);
        }

        public OperationType OperationType
        {
            get => _operationType;
            set => SetProperty(ref _operationType, value);
        }

        public string Module
        {
            get => _module;
            set => SetProperty(ref _module, value);
        }

        public string Description
        {
            get => _description;
            set => SetProperty(ref _description, value);
        }

        public string TargetId
        {
            get => _targetId;
            set => SetProperty(ref _targetId, value);
        }

        public string TargetName
        {
            get => _targetName;
            set => SetProperty(ref _targetName, value);
        }

        public string IpAddress
        {
            get => _ipAddress;
            set => SetProperty(ref _ipAddress, value);
        }

        public bool Success
        {
            get => _success;
            set => SetProperty(ref _success, value);
        }

        public string ErrorMessage
        {
            get => _errorMessage;
            set => SetProperty(ref _errorMessage, value);
        }

        public string OperationTypeText => OperationType switch
        {
            OperationType.Create => "创建",
            OperationType.Update => "更新",
            OperationType.Delete => "删除",
            OperationType.View => "查看",
            OperationType.Export => "导出",
            OperationType.Import => "导入",
            OperationType.Login => "登录",
            OperationType.Logout => "登出",
            _ => "未知"
        };

        public string StatusText => Success ? "成功" : "失败";

        public event PropertyChangedEventHandler? PropertyChanged;

        protected virtual void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        protected bool SetProperty<T>(ref T field, T value, [CallerMemberName] string? propertyName = null)
        {
            if (Equals(field, value)) return false;
            field = value;
            OnPropertyChanged(propertyName);
            return true;
        }
    }
}