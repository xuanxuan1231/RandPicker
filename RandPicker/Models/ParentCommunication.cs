using System;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace RandPicker.Models
{
    /// <summary>
    /// 沟通类型枚举
    /// </summary>
    public enum CommunicationType
    {
        Phone,      // 电话
        Message,    // 短信
        Email,      // 邮件
        Meeting,    // 面谈
        WeChat,     // 微信
        Other       // 其他
    }

    /// <summary>
    /// 家长沟通记录模型
    /// </summary>
    public class ParentCommunication : INotifyPropertyChanged
    {
        private string _id = Guid.NewGuid().ToString();
        private string _studentId = string.Empty;
        private string _studentName = string.Empty;
        private string _parentName = string.Empty;
        private string _parentPhone = string.Empty;
        private DateTime _communicationDate = DateTime.Now;
        private CommunicationType _communicationType = CommunicationType.Phone;
        private string _topic = string.Empty;
        private string _content = string.Empty;
        private string _teacherName = string.Empty;
        private string _followUpAction = string.Empty;
        private DateTime? _nextFollowUpDate;
        private bool _isResolved = false;

        public string Id
        {
            get => _id;
            set => SetProperty(ref _id, value);
        }

        public string StudentId
        {
            get => _studentId;
            set => SetProperty(ref _studentId, value);
        }

        public string StudentName
        {
            get => _studentName;
            set => SetProperty(ref _studentName, value);
        }

        public string ParentName
        {
            get => _parentName;
            set => SetProperty(ref _parentName, value);
        }

        public string ParentPhone
        {
            get => _parentPhone;
            set => SetProperty(ref _parentPhone, value);
        }

        public DateTime CommunicationDate
        {
            get => _communicationDate;
            set => SetProperty(ref _communicationDate, value);
        }

        public CommunicationType CommunicationType
        {
            get => _communicationType;
            set => SetProperty(ref _communicationType, value);
        }

        public string Topic
        {
            get => _topic;
            set => SetProperty(ref _topic, value);
        }

        public string Content
        {
            get => _content;
            set => SetProperty(ref _content, value);
        }

        public string TeacherName
        {
            get => _teacherName;
            set => SetProperty(ref _teacherName, value);
        }

        public string FollowUpAction
        {
            get => _followUpAction;
            set => SetProperty(ref _followUpAction, value);
        }

        public DateTime? NextFollowUpDate
        {
            get => _nextFollowUpDate;
            set => SetProperty(ref _nextFollowUpDate, value);
        }

        public bool IsResolved
        {
            get => _isResolved;
            set => SetProperty(ref _isResolved, value);
        }

        public string CommunicationTypeText => CommunicationType switch
        {
            CommunicationType.Phone => "电话",
            CommunicationType.Message => "短信",
            CommunicationType.Email => "邮件",
            CommunicationType.Meeting => "面谈",
            CommunicationType.WeChat => "微信",
            CommunicationType.Other => "其他",
            _ => "未知"
        };

        public string StatusText => IsResolved ? "已解决" : "待跟进";

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