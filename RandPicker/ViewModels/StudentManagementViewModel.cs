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
    /// 学生管理视图模型
    /// </summary>
    public partial class StudentManagementViewModel : ViewModelBase
    {
        private readonly StudentManagementService _studentService;
        private readonly DataService _dataService;

        [ObservableProperty]
        private ObservableCollection<StudentProfile> _studentProfiles = new();

        [ObservableProperty]
        private ObservableCollection<AttendanceRecord> _attendanceRecords = new();

        [ObservableProperty]
        private ObservableCollection<GradeRecord> _gradeRecords = new();

        [ObservableProperty]
        private StudentProfile? _selectedStudent;

        [ObservableProperty]
        private string _searchKeyword = string.Empty;

        [ObservableProperty]
        private bool _isLoading = false;

        [ObservableProperty]
        private string _statusMessage = string.Empty;

        public ICommand LoadDataCommand { get; }
        public ICommand SearchCommand { get; }
        public ICommand AddStudentCommand { get; }
        public ICommand EditStudentCommand { get; }
        public ICommand DeleteStudentCommand { get; }
        public ICommand RefreshCommand { get; }

        public StudentManagementViewModel()
        {
            _dataService = new DataService();
            _studentService = new StudentManagementService(_dataService);

            LoadDataCommand = new AsyncRelayCommand(LoadDataAsync);
            SearchCommand = new AsyncRelayCommand(SearchStudentsAsync);
            AddStudentCommand = new RelayCommand(AddStudent);
            EditStudentCommand = new RelayCommand(EditStudent, () => SelectedStudent != null);
            DeleteStudentCommand = new AsyncRelayCommand(DeleteStudentAsync, () => SelectedStudent != null);
            RefreshCommand = new AsyncRelayCommand(RefreshDataAsync);

            // 初始化时加载数据
            _ = Task.Run(LoadDataAsync);
        }

        private async Task LoadDataAsync()
        {
            try
            {
                IsLoading = true;
                StatusMessage = "正在加载数据...";

                var profiles = await _studentService.GetAllStudentProfilesAsync();
                
                StudentProfiles.Clear();
                foreach (var profile in profiles)
                {
                    StudentProfiles.Add(profile);
                }

                StatusMessage = $"已加载 {StudentProfiles.Count} 名学生";
                Log.Information($"成功加载 {StudentProfiles.Count} 名学生档案");
            }
            catch (Exception ex)
            {
                StatusMessage = $"加载数据失败: {ex.Message}";
                Log.Error($"加载学生数据时出错: {ex.Message}");
            }
            finally
            {
                IsLoading = false;
            }
        }

        private async Task SearchStudentsAsync()
        {
            try
            {
                IsLoading = true;
                StatusMessage = "正在搜索...";

                var results = await _studentService.SearchStudentProfilesAsync(SearchKeyword);
                
                StudentProfiles.Clear();
                foreach (var profile in results)
                {
                    StudentProfiles.Add(profile);
                }

                StatusMessage = $"找到 {StudentProfiles.Count} 名学生";
            }
            catch (Exception ex)
            {
                StatusMessage = $"搜索失败: {ex.Message}";
                Log.Error($"搜索学生时出错: {ex.Message}");
            }
            finally
            {
                IsLoading = false;
            }
        }

        private void AddStudent()
        {
            // 这里应该打开添加学生的对话框
            // 暂时创建一个示例学生
            var newStudent = new StudentProfile
            {
                StudentId = GenerateStudentId(),
                Name = "新学生",
                EnrollmentDate = DateTime.Today,
                IsActive = true
            };

            SelectedStudent = newStudent;
            StatusMessage = "请填写学生信息";
        }

        private void EditStudent()
        {
            if (SelectedStudent == null) return;
            
            StatusMessage = $"正在编辑学生: {SelectedStudent.Name}";
        }

        private async Task DeleteStudentAsync()
        {
            if (SelectedStudent == null) return;

            try
            {
                IsLoading = true;
                StatusMessage = $"正在删除学生: {SelectedStudent.Name}";

                var success = await _studentService.DeleteStudentProfileAsync(SelectedStudent.StudentId);
                
                if (success)
                {
                    StudentProfiles.Remove(SelectedStudent);
                    SelectedStudent = null;
                    StatusMessage = "学生删除成功";
                }
                else
                {
                    StatusMessage = "删除学生失败";
                }
            }
            catch (Exception ex)
            {
                StatusMessage = $"删除学生失败: {ex.Message}";
                Log.Error($"删除学生时出错: {ex.Message}");
            }
            finally
            {
                IsLoading = false;
            }
        }

        private async Task RefreshDataAsync()
        {
            SearchKeyword = string.Empty;
            await LoadDataAsync();
        }

        private string GenerateStudentId()
        {
            var year = DateTime.Now.Year.ToString();
            var random = new Random();
            var number = random.Next(1000, 9999);
            return $"{year}{number}";
        }

        partial void OnSelectedStudentChanged(StudentProfile? value)
        {
            // 当选中的学生改变时，更新命令的可执行状态
            ((RelayCommand)EditStudentCommand).NotifyCanExecuteChanged();
            ((AsyncRelayCommand)DeleteStudentCommand).NotifyCanExecuteChanged();
        }
    }
}