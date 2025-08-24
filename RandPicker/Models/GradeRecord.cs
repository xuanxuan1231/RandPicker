using System;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace RandPicker.Models
{
    /// <summary>
    /// 成绩记录模型
    /// </summary>
    public class GradeRecord : INotifyPropertyChanged
    {
        private string _studentId = string.Empty;
        private string _studentName = string.Empty;
        private string _subject = string.Empty;
        private string _examType = string.Empty;
        private double _score;
        private double _fullScore = 100;
        private DateTime _examDate = DateTime.Today;
        private string _semester = string.Empty;
        private string _remarks = string.Empty;
        private int _ranking;

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

        public string ExamType
        {
            get => _examType;
            set => SetProperty(ref _examType, value);
        }

        public double Score
        {
            get => _score;
            set => SetProperty(ref _score, value);
        }

        public double FullScore
        {
            get => _fullScore;
            set => SetProperty(ref _fullScore, value);
        }

        public DateTime ExamDate
        {
            get => _examDate;
            set => SetProperty(ref _examDate, value);
        }

        public string Semester
        {
            get => _semester;
            set => SetProperty(ref _semester, value);
        }

        public string Remarks
        {
            get => _remarks;
            set => SetProperty(ref _remarks, value);
        }

        public int Ranking
        {
            get => _ranking;
            set => SetProperty(ref _ranking, value);
        }

        public double Percentage => FullScore > 0 ? (Score / FullScore) * 100 : 0;

        public string Grade
        {
            get
            {
                var percentage = Percentage;
                return percentage switch
                {
                    >= 90 => "优秀",
                    >= 80 => "良好",
                    >= 70 => "中等",
                    >= 60 => "及格",
                    _ => "不及格"
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