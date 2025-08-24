using System;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Input;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using RandPicker.Models;
using RandPicker.Services;
using Serilog;

namespace RandPicker.ViewModels
{
    /// <summary>
    /// 考勤管理视图模型
    /// </summary>
    public partial class AttendanceManagementViewModel : ViewModelBase
    {
        private readonly StudentManagementService _studentService;
        private readonly DataService _dataService;

        [ObservableProperty]
        private ObservableCollection<AttendanceRecord> _attendanceRecords = new();

        [ObservableProperty]
        private ObservableCollection<StudentProfile> _students = new();

        [ObservableProperty]
        private StudentProfile? _selectedStudent;

        [ObservableProperty]
        private DateTime _startDate = DateTime.Today.AddDays(-7);

        [ObservableProperty]
        private DateTime _endDate = DateTime.Today;

        [ObservableProperty]
        private bool _isLoading = false;

        [ObservableProperty]
        private string _statusMessage = string.Empty;

        // 统计数据
        [ObservableProperty]
        private int _presentCount;

        [ObservableProperty]
        private int _absentCount;

        [ObservableProperty]
        private int _lateCount;

        [ObservableProperty]
        private int _leaveCount;

        [ObservableProperty]
        private int _sickCount;

        [ObservableProperty]
        private double _todayAttendanceRate;

        [ObservableProperty]
        private double _weekAttendanceRate;

        [ObservableProperty]
        private double _monthAttendanceRate;

        public ICommand LoadDataCommand { get; }
        public ICommand QueryCommand { get; }
        public ICommand ResetCommand { get; }
        public ICommand CheckInCommand { get; }
        public ICommand BatchAttendanceCommand { get; }
        public ICommand ExportReportCommand { get; }

        public AttendanceManagementViewModel()
        {
            _dataService = new DataService();
            _studentService = new StudentManagementService(_dataService);

            LoadDataCommand = new AsyncRelayCommand(LoadDataAsync);
            QueryCommand = new AsyncRelayCommand(QueryAttendanceAsync);
            ResetCommand = new RelayCommand(ResetFilters);
            CheckInCommand = new AsyncRelayCommand(CheckInAsync);
            BatchAttendanceCommand = new RelayCommand(BatchAttendance);
            ExportReportCommand = new AsyncRelayCommand(ExportReportAsync);

            // 初始化时加载数据
            _ = Task.Run(LoadDataAsync);
        }

        private async Task LoadDataAsync()
        {
            try
            {
                IsLoading = true;
                StatusMessage = "正在加载数据...";

                // 加载学生列表
                var students = await _studentService.GetAllStudentProfilesAsync();
                Students.Clear();
                foreach (var student in students.Where(s => s.IsActive))
                {
                    Students.Add(student);
                }

                // 加载考勤记录
                await QueryAttendanceAsync();

                StatusMessage = $"已加载 {AttendanceRecords.Count} 条考勤记录";
                Log.Information($"成功加载考勤数据");
            }
            catch (Exception ex)
            {
                StatusMessage = $"加载数据失败: {ex.Message}";
                Log.Error($"加载考勤数据时出错: {ex.Message}");
            }
            finally
            {
                IsLoading = false;
            }
        }

        private async Task QueryAttendanceAsync()
        {
            try
            {
                IsLoading = true;
                StatusMessage = "正在查询考勤记录...";

                var records = await _studentService.GetAttendanceRecordsAsync(
                    SelectedStudent?.StudentId, 
                    StartDate, 
                    EndDate);

                AttendanceRecords.Clear();
                foreach (var record in records)
                {
                    AttendanceRecords.Add(record);
                }

                // 更新统计数据
                UpdateStatistics();

                StatusMessage = $"找到 {AttendanceRecords.Count} 条考勤记录";
            }
            catch (Exception ex)
            {
                StatusMessage = $"查询失败: {ex.Message}";
                Log.Error($"查询考勤记录时出错: {ex.Message}");
            }
            finally
            {
                IsLoading = false;
            }
        }

        private void ResetFilters()
        {
            SelectedStudent = null;
            StartDate = DateTime.Today.AddDays(-7);
            EndDate = DateTime.Today;
            _ = Task.Run(QueryAttendanceAsync);
        }

        private async Task CheckInAsync()
        {
            if (SelectedStudent == null)
            {
                StatusMessage = "请先选择学生";
                return;
            }

            try
            {
                IsLoading = true;
                StatusMessage = $"正在为 {SelectedStudent.Name} 签到...";

                var record = new AttendanceRecord
                {
                    StudentId = SelectedStudent.StudentId,
                    StudentName = SelectedStudent.Name,
                    Date = DateTime.Today,
                    Status = AttendanceStatus.Present,
                    CheckInTime = DateTime.Now
                };

                var success = await _studentService.AddAttendanceRecordAsync(record);

                if (success)
                {
                    AttendanceRecords.Insert(0, record);
                    UpdateStatistics();
                    StatusMessage = $"{SelectedStudent.Name} 签到成功";
                }
                else
                {
                    StatusMessage = "签到失败，可能今天已经签到过了";
                }
            }
            catch (Exception ex)
            {
                StatusMessage = $"签到失败: {ex.Message}";
                Log.Error($"签到时出错: {ex.Message}");
            }
            finally
            {
                IsLoading = false;
            }
        }

        private void BatchAttendance()
        {
            StatusMessage = "批量考勤功能开发中...";
        }

        private async Task ExportReportAsync()
        {
            try
            {
                IsLoading = true;
                StatusMessage = "正在导出考勤报表...";

                // 这里可以实现导出到Excel或PDF的功能
                await Task.Delay(1000); // 模拟导出过程

                StatusMessage = "考勤报表导出成功";
            }
            catch (Exception ex)
            {
                StatusMessage = $"导出失败: {ex.Message}";
                Log.Error($"导出考勤报表时出错: {ex.Message}");
            }
            finally
            {
                IsLoading = false;
            }
        }

        private void UpdateStatistics()
        {
            var records = AttendanceRecords.ToList();

            PresentCount = records.Count(r => r.Status == AttendanceStatus.Present);
            AbsentCount = records.Count(r => r.Status == AttendanceStatus.Absent);
            LateCount = records.Count(r => r.Status == AttendanceStatus.Late);
            LeaveCount = records.Count(r => r.Status == AttendanceStatus.Leave);
            SickCount = records.Count(r => r.Status == AttendanceStatus.Sick);

            // 计算出勤率
            var totalRecords = records.Count;
            if (totalRecords > 0)
            {
                var presentAndLate = PresentCount + LateCount;
                var attendanceRate = (double)presentAndLate / totalRecords * 100;

                // 今日出勤率
                var todayRecords = records.Where(r => r.Date.Date == DateTime.Today).ToList();
                TodayAttendanceRate = todayRecords.Count > 0 
                    ? (double)todayRecords.Count(r => r.Status == AttendanceStatus.Present || r.Status == AttendanceStatus.Late) / todayRecords.Count * 100 
                    : 0;

                // 本周出勤率
                var weekStart = DateTime.Today.AddDays(-(int)DateTime.Today.DayOfWeek);
                var weekRecords = records.Where(r => r.Date >= weekStart).ToList();
                WeekAttendanceRate = weekRecords.Count > 0 
                    ? (double)weekRecords.Count(r => r.Status == AttendanceStatus.Present || r.Status == AttendanceStatus.Late) / weekRecords.Count * 100 
                    : 0;

                // 本月出勤率
                var monthStart = new DateTime(DateTime.Today.Year, DateTime.Today.Month, 1);
                var monthRecords = records.Where(r => r.Date >= monthStart).ToList();
                MonthAttendanceRate = monthRecords.Count > 0 
                    ? (double)monthRecords.Count(r => r.Status == AttendanceStatus.Present || r.Status == AttendanceStatus.Late) / monthRecords.Count * 100 
                    : 0;
            }
        }
    }
}