using System;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Timers;
using RandPicker.Views;

namespace RandPicker.ViewModels
{
    /// <summary>
    /// 主仪表板视图模型
    /// </summary>
    public class MainDashboardViewModel : ViewModelBase
    {
        private DateTime _currentTime = DateTime.Now;
        private readonly Timer _timer;

        public DateTime CurrentTime
        {
            get => _currentTime;
            set => SetProperty(ref _currentTime, value);
        }

        // 各个管理模块的视图
        public StudentManagementView StudentManagementView { get; }
        public AttendanceManagementView AttendanceManagementView { get; }
        public GradeManagementView GradeManagementView { get; }

        public MainDashboardViewModel()
        {
            // 初始化各个管理视图
            StudentManagementView = new StudentManagementView();
            AttendanceManagementView = new AttendanceManagementView();
            GradeManagementView = new GradeManagementView();

            // 设置定时器更新当前时间
            _timer = new Timer(1000); // 每秒更新一次
            _timer.Elapsed += OnTimerElapsed;
            _timer.Start();
        }

        private void OnTimerElapsed(object? sender, ElapsedEventArgs e)
        {
            CurrentTime = DateTime.Now;
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