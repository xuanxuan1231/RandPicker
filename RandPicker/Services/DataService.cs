using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using RandPicker.Models;
using Serilog;

namespace RandPicker.Services
{
    /// <summary>
    /// 数据服务类 - 处理所有数据的持久化操作
    /// </summary>
    public class DataService
    {
        private readonly string _dataDirectory;
        private readonly JsonSerializerOptions _jsonOptions;

        public DataService()
        {
            var baseDir = Path.GetDirectoryName(Environment.ProcessPath) ?? AppDomain.CurrentDomain.BaseDirectory;
            _dataDirectory = Path.Combine(baseDir, "Data");
            
            // 确保数据目录存在
            if (!Directory.Exists(_dataDirectory))
            {
                Directory.CreateDirectory(_dataDirectory);
            }

            _jsonOptions = new JsonSerializerOptions
            {
                WriteIndented = true,
                Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
            };
        }

        #region 通用方法

        private async Task<List<T>> LoadDataAsync<T>(string fileName)
        {
            try
            {
                var filePath = Path.Combine(_dataDirectory, fileName);
                if (!File.Exists(filePath))
                {
                    return new List<T>();
                }

                var jsonString = await File.ReadAllTextAsync(filePath);
                var data = JsonSerializer.Deserialize<List<T>>(jsonString, _jsonOptions);
                return data ?? new List<T>();
            }
            catch (Exception ex)
            {
                Log.Error($"加载数据文件 {fileName} 时出错: {ex.Message}");
                return new List<T>();
            }
        }

        private async Task<bool> SaveDataAsync<T>(List<T> data, string fileName)
        {
            try
            {
                var filePath = Path.Combine(_dataDirectory, fileName);
                var jsonString = JsonSerializer.Serialize(data, _jsonOptions);
                await File.WriteAllTextAsync(filePath, jsonString);
                Log.Information($"成功保存 {data.Count} 条记录到 {fileName}");
                return true;
            }
            catch (Exception ex)
            {
                Log.Error($"保存数据文件 {fileName} 时出错: {ex.Message}");
                return false;
            }
        }

        #endregion

        #region 学生档案管理

        public async Task<List<StudentProfile>> LoadStudentProfilesAsync()
        {
            return await LoadDataAsync<StudentProfile>("student_profiles.json");
        }

        public async Task<bool> SaveStudentProfilesAsync(List<StudentProfile> profiles)
        {
            return await SaveDataAsync(profiles, "student_profiles.json");
        }

        #endregion

        #region 考勤记录管理

        public async Task<List<AttendanceRecord>> LoadAttendanceRecordsAsync()
        {
            return await LoadDataAsync<AttendanceRecord>("attendance_records.json");
        }

        public async Task<bool> SaveAttendanceRecordsAsync(List<AttendanceRecord> records)
        {
            return await SaveDataAsync(records, "attendance_records.json");
        }

        #endregion

        #region 成绩记录管理

        public async Task<List<GradeRecord>> LoadGradeRecordsAsync()
        {
            return await LoadDataAsync<GradeRecord>("grade_records.json");
        }

        public async Task<bool> SaveGradeRecordsAsync(List<GradeRecord> records)
        {
            return await SaveDataAsync(records, "grade_records.json");
        }

        #endregion

        #region 学习进度管理

        public async Task<List<LearningProgress>> LoadLearningProgressAsync()
        {
            return await LoadDataAsync<LearningProgress>("learning_progress.json");
        }

        public async Task<bool> SaveLearningProgressAsync(List<LearningProgress> progress)
        {
            return await SaveDataAsync(progress, "learning_progress.json");
        }

        #endregion

        #region 行为评估管理

        public async Task<List<BehaviorAssessment>> LoadBehaviorAssessmentsAsync()
        {
            return await LoadDataAsync<BehaviorAssessment>("behavior_assessments.json");
        }

        public async Task<bool> SaveBehaviorAssessmentsAsync(List<BehaviorAssessment> assessments)
        {
            return await SaveDataAsync(assessments, "behavior_assessments.json");
        }

        #endregion

        #region 家长沟通记录管理

        public async Task<List<ParentCommunication>> LoadParentCommunicationsAsync()
        {
            return await LoadDataAsync<ParentCommunication>("parent_communications.json");
        }

        public async Task<bool> SaveParentCommunicationsAsync(List<ParentCommunication> communications)
        {
            return await SaveDataAsync(communications, "parent_communications.json");
        }

        #endregion

        #region 操作日志管理

        public async Task<List<OperationLog>> LoadOperationLogsAsync()
        {
            return await LoadDataAsync<OperationLog>("operation_logs.json");
        }

        public async Task<bool> SaveOperationLogsAsync(List<OperationLog> logs)
        {
            return await SaveDataAsync(logs, "operation_logs.json");
        }

        public async Task<bool> AddOperationLogAsync(OperationLog log)
        {
            var logs = await LoadOperationLogsAsync();
            logs.Add(log);
            return await SaveOperationLogsAsync(logs);
        }

        #endregion
    }
}