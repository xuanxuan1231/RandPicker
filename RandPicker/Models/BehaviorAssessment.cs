using System;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace RandPicker.Models
{
    /// <summary>
    /// 行为类型枚举
    /// </summary>
    public enum BehaviorType
    {
        Positive = 1,   // 积极行为
        Negative = -1,  // 消极行为
        Neutral = 0     // 中性行为
    }

    /// <summary>
    /// 行为表现评估模型
    /// </summary>
    public class BehaviorAssessment : INotifyPropertyChanged
    {
        private string _studentId = string.Empty;
        private string _studentName = string.Empty;
        private DateTime _date = DateTime.Today;
        private BehaviorType _behaviorType = BehaviorType.Positive;
        private string _category = string.Empty;
        private string _description = string.Empty;
        private int _score;
        private string _teacher = string.Empty;
        private string _remarks = string.Empty;

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

        public DateTime Date
        {
            get => _date;
            set => SetProperty(ref _date, value);
        }

        public BehaviorType BehaviorType
        {
            get => _behaviorType;
            set => SetProperty(ref _behaviorType, value);
        }

        public string Category
        {
            get => _category;
            set => SetProperty(ref _category, value);
        }

        public string Description
        {
            get => _description;
            set => SetProperty(ref _description, value);
        }

        public int Score
        {
            get => _score;
            set => SetProperty(ref _score, value);
        }

        public string Teacher
        {
            get => _teacher;
            set => SetProperty(ref _teacher, value);
        }

        public string Remarks
        {
            get => _remarks;
            set => SetProperty(ref _remarks, value);
        }

        public string BehaviorTypeText => BehaviorType switch
        {
            BehaviorType.Positive => "积极行为",
            BehaviorType.Negative => "消极行为",
            BehaviorType.Neutral => "中性行为",
            _ => "未知"
        };

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