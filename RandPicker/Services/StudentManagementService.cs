using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using RandPicker.Models;
using Serilog;

namespace RandPicker.Services
{
    /// <summary>
    /// 学生管理服务类 - 处理学生管理相关的业务逻辑
    /// </summary>
    public class StudentManagementService
    {
        private readonly DataService _dataService;

        public StudentManagementService(DataService dataService)
        {
            _dataService = dataService;
        }

        #region 学生档案管理

        public async Task<List<StudentProfile>> GetAllStudentProfilesAsync()
        {
            return await _dataService.LoadStudentProfilesAsync();
        }

        public async Task<StudentProfile?> GetStudentProfileByIdAsync(string studentId)
        {
            var profiles = await _dataService.LoadStudentProfilesAsync();
            return profiles.FirstOrDefault(p => p.StudentId == studentId);
        }

        public async Task<bool> AddStudentProfileAsync(StudentProfile profile)
        {
            var profiles = await _dataService.LoadStudentProfilesAsync();
            
            // 检查学号是否已存在
            if (profiles.Any(p => p.StudentId == profile.StudentId))
            {
                Log.Warning($"学号 {profile.StudentId} 已存在");
                return false;
            }

            profiles.Add(profile);
            var result = await _dataService.SaveStudentProfilesAsync(profiles);
            
            if (result)
            {
                await LogOperationAsync("学生档案", OperationType.Create, profile.StudentId, profile.Name, "添加学生档案");
            }
            
            return result;
        }

        public async Task<bool> UpdateStudentProfileAsync(StudentProfile profile)
        {
            var profiles = await _dataService.LoadStudentProfilesAsync();
            var existingProfile = profiles.FirstOrDefault(p => p.StudentId == profile.StudentId);
            
            if (existingProfile == null)
            {
                Log.Warning($"未找到学号为 {profile.StudentId} 的学生");
                return false;
            }

            var index = profiles.IndexOf(existingProfile);
            profiles[index] = profile;
            
            var result = await _dataService.SaveStudentProfilesAsync(profiles);
            
            if (result)
            {
                await LogOperationAsync("学生档案", OperationType.Update, profile.StudentId, profile.Name, "更新学生档案");
            }
            
            return result;
        }

        public async Task<bool> DeleteStudentProfileAsync(string studentId)
        {
            var profiles = await _dataService.LoadStudentProfilesAsync();
            var profile = profiles.FirstOrDefault(p => p.StudentId == studentId);
            
            if (profile == null)
            {
                Log.Warning($"未找到学号为 {studentId} 的学生");
                return false;
            }

            profiles.Remove(profile);
            var result = await _dataService.SaveStudentProfilesAsync(profiles);
            
            if (result)
            {
                await LogOperationAsync("学生档案", OperationType.Delete, studentId, profile.Name, "删除学生档案");
            }
            
            return result;
        }

        public async Task<List<StudentProfile>> SearchStudentProfilesAsync(string keyword)
        {
            var profiles = await _dataService.LoadStudentProfilesAsync();
            
            if (string.IsNullOrWhiteSpace(keyword))
            {
                return profiles;
            }

            return profiles.Where(p => 
                p.Name.Contains(keyword, StringComparison.OrdinalIgnoreCase) ||
                p.StudentId.Contains(keyword, StringComparison.OrdinalIgnoreCase) ||
                p.ClassName.Contains(keyword, StringComparison.OrdinalIgnoreCase) ||
                p.Grade.Contains(keyword, StringComparison.OrdinalIgnoreCase)
            ).ToList();
        }

        #endregion

        #region 考勤管理

        public async Task<List<AttendanceRecord>> GetAttendanceRecordsAsync(string? studentId = null, DateTime? startDate = null, DateTime? endDate = null)
        {
            var records = await _dataService.LoadAttendanceRecordsAsync();
            
            if (!string.IsNullOrEmpty(studentId))
            {
                records = records.Where(r => r.StudentId == studentId).ToList();
            }
            
            if (startDate.HasValue)
            {
                records = records.Where(r => r.Date >= startDate.Value).ToList();
            }
            
            if (endDate.HasValue)
            {
                records = records.Where(r => r.Date <= endDate.Value).ToList();
            }
            
            return records.OrderByDescending(r => r.Date).ToList();
        }

        public async Task<bool> AddAttendanceRecordAsync(AttendanceRecord record)
        {
            var records = await _dataService.LoadAttendanceRecordsAsync();
            
            // 检查是否已有当天的考勤记录
            var existingRecord = records.FirstOrDefault(r => 
                r.StudentId == record.StudentId && r.Date.Date == record.Date.Date);
            
            if (existingRecord != null)
            {
                Log.Warning($"学生 {record.StudentId} 在 {record.Date:yyyy-MM-dd} 已有考勤记录");
                return false;
            }

            records.Add(record);
            var result = await _dataService.SaveAttendanceRecordsAsync(records);
            
            if (result)
            {
                await LogOperationAsync("考勤记录", OperationType.Create, record.StudentId, record.StudentName, $"添加考勤记录 - {record.StatusText}");
            }
            
            return result;
        }

        public async Task<Dictionary<AttendanceStatus, int>> GetAttendanceStatisticsAsync(string studentId, DateTime startDate, DateTime endDate)
        {
            var records = await GetAttendanceRecordsAsync(studentId, startDate, endDate);
            
            return records.GroupBy(r => r.Status)
                         .ToDictionary(g => g.Key, g => g.Count());
        }

        #endregion

        #region 成绩管理

        public async Task<List<GradeRecord>> GetGradeRecordsAsync(string? studentId = null, string? subject = null, string? semester = null)
        {
            var records = await _dataService.LoadGradeRecordsAsync();
            
            if (!string.IsNullOrEmpty(studentId))
            {
                records = records.Where(r => r.StudentId == studentId).ToList();
            }
            
            if (!string.IsNullOrEmpty(subject))
            {
                records = records.Where(r => r.Subject.Contains(subject, StringComparison.OrdinalIgnoreCase)).ToList();
            }
            
            if (!string.IsNullOrEmpty(semester))
            {
                records = records.Where(r => r.Semester == semester).ToList();
            }
            
            return records.OrderByDescending(r => r.ExamDate).ToList();
        }

        public async Task<bool> AddGradeRecordAsync(GradeRecord record)
        {
            var records = await _dataService.LoadGradeRecordsAsync();
            records.Add(record);
            
            var result = await _dataService.SaveGradeRecordsAsync(records);
            
            if (result)
            {
                await LogOperationAsync("成绩记录", OperationType.Create, record.StudentId, record.StudentName, $"添加成绩记录 - {record.Subject}: {record.Score}分");
            }
            
            return result;
        }

        public async Task<Dictionary<string, double>> GetSubjectAveragesAsync(string studentId)
        {
            var records = await GetGradeRecordsAsync(studentId);
            
            return records.GroupBy(r => r.Subject)
                         .ToDictionary(g => g.Key, g => g.Average(r => r.Score));
        }

        #endregion

        #region 私有方法

        private async Task LogOperationAsync(string module, OperationType operationType, string targetId, string targetName, string description)
        {
            var log = new OperationLog
            {
                Module = module,
                OperationType = operationType,
                TargetId = targetId,
                TargetName = targetName,
                Description = description,
                UserName = "系统管理员", // 这里可以根据实际登录用户设置
                Success = true
            };
            
            await _dataService.AddOperationLogAsync(log);
        }

        #endregion
    }
}