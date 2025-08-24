using System;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace RandPicker.Models
{
    /// <summary>
    /// 考勤状态枚举
    /// </summary>
    public enum AttendanceStatus
    {
        Present = 0,    // 出勤
        Absent = 1,     // 缺勤
        Late = 2,       // 迟到
        Leave = 3,      // 请假
        Sick = 4        // 病假
    }

    /// <summary>
    /// 考勤记录模型
    /// </summary>
    public class AttendanceRecord : INotifyPropertyChanged
    {
        private string _studentId = string.Empty;
        private string _studentName = string.Empty;
        private DateTime _date = DateTime.Today;
        private AttendanceStatus _status = AttendanceStatus.Present;
        private string _remarks = string.Empty;
        private DateTime? _checkInTime;
        private DateTime? _checkOutTime;

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

        public AttendanceStatus Status
        {
            get => _status;
            set => SetProperty(ref _status, value);
        }

        public string Remarks
        {
            get => _remarks;
            set => SetProperty(ref _remarks, value);
        }

        public DateTime? CheckInTime
        {
            get => _checkInTime;
            set => SetProperty(ref _checkInTime, value);
        }

        public DateTime? CheckOutTime
        {
            get => _checkOutTime;
            set => SetProperty(ref _checkOutTime, value);
        }

        public string StatusText => Status switch
        {
            AttendanceStatus.Present => "出勤",
            AttendanceStatus.Absent => "缺勤",
            AttendanceStatus.Late => "迟到",
            AttendanceStatus.Leave => "请假",
            AttendanceStatus.Sick => "病假",
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