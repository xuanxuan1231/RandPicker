using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace RandPicker.Models
{
    /// <summary>
    /// 学习进度模型
    /// </summary>
    public class LearningProgress : INotifyPropertyChanged
    {
        private string _studentId = string.Empty;
        private string _studentName = string.Empty;
        private string _subject = string.Empty;
        private string _chapter = string.Empty;
        private string _topic = string.Empty;
        private double _completionRate;
        private DateTime _startDate = DateTime.Today;
        private DateTime? _completionDate;
        private string _status = string.Empty;
        private string _notes = string.Empty;
        private int _studyHours;

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

        public string Subject
        {
            get => _subject;
            set => SetProperty(ref _subject, value);
        }

        public string Chapter
        {
            get => _chapter;
            set => SetProperty(ref _chapter, value);
        }

        public string Topic
        {
            get => _topic;
            set => SetProperty(ref _topic, value);
        }

        public double CompletionRate
        {
            get => _completionRate;
            set => SetProperty(ref _completionRate, Math.Max(0, Math.Min(100, value)));
        }

        public DateTime StartDate
        {
            get => _startDate;
            set => SetProperty(ref _startDate, value);
        }

        public DateTime? CompletionDate
        {
            get => _completionDate;
            set => SetProperty(ref _completionDate, value);
        }

        public string Status
        {
            get => _status;
            set => SetProperty(ref _status, value);
        }

        public string Notes
        {
            get => _notes;
            set => SetProperty(ref _notes, value);
        }

        public int StudyHours
        {
            get => _studyHours;
            set => SetProperty(ref _studyHours, Math.Max(0, value));
        }

        public bool IsCompleted => CompletionRate >= 100;

        public string ProgressStatus
        {
            get
            {
                return CompletionRate switch
                {
                    100 => "已完成",
                    >= 80 => "接近完成",
                    >= 50 => "进行中",
                    >= 20 => "刚开始",
                    _ => "未开始"
                };
            }
        }

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