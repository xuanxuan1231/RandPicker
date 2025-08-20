using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;
using Serilog;

namespace RandPicker.Models;

/// <summary>
/// 学生信息类
/// </summary>
public class Student
{
    [JsonPropertyName("name")] public string Name { get; set; } = string.Empty;

    [JsonPropertyName("id")] public int Id { get; set; }

    [JsonPropertyName("weight")] public int Weight { get; set; } = 1;

    [JsonPropertyName("active")] public bool IsActive { get; set; } = true;

    public override string ToString() => $"{Name} ({Id})";
}

/// <summary>
/// 学生列表类
/// </summary>
public class StudentData
{
    [JsonPropertyName("students")] public List<Student> Students { get; set; } = new();
}

/// <summary>
/// 学生数据服务类 数据处理有关
/// </summary>
public static class StudentService
{
    /// <summary>
    /// 加载学生数据
    /// </summary>
    public static List<Student> LoadFromJson(string filepath)
    {
        try
        {
            if (!File.Exists(filepath))
            {
                Log.Warning("学生文件不存在。创建一个新的。");
                File.WriteAllText(filepath, "{\"students\": [], \"groups\": []}");
            }

            var jsonString = File.ReadAllText(filepath);
            var studentData = JsonSerializer.Deserialize<StudentData>(jsonString);

            var students = studentData?.Students ?? new List<Student>();
            Log.Information($"加载了 {students.Count} 名学生。");
            return students;
        }
        catch (Exception ex)
        {
            Log.Error($"加载学生数据时出错: {ex.Message}");
            return new List<Student>();
        }
    }

    /// <summary>
    /// 保存
    /// </summary>
    /// <param name="students">学生列表</param>
    /// <param name="filepath">保存路径</param>
    public static async Task<bool> SaveToJson(List<Student> students, string filepath)
    {
        try
        {
            var studentData = new StudentData { Students = students };
            var options = new JsonSerializerOptions
            {
                WriteIndented = true,
                Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
            };

            var jsonString = JsonSerializer.Serialize(studentData, options);
            await File.WriteAllTextAsync(filepath, jsonString);

            Console.WriteLine($"成功保存 {students.Count} 名学生。");
            return true;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"保存学生数据时出错: {ex.Message}");
            return false;
        }
    }

    /// <summary>
    /// 获取活跃的学生列表
    /// </summary>
    public static List<Student> GetActiveList(List<Student> students)
    {
        return students.Where(s => s.IsActive).ToList();
    }

    /// <summary>
    /// 根据权重加工列表
    /// </summary>
    /// <param name="students">学生列表</param>
    /// <returns>加权学生列表</returns>
    public static List<Student> GetWeightedList(List<Student> students)
    {
        var weightedList = new List<Student>();

        foreach (var student in students)
        {
            for (int i = 0; i < Math.Max(1, student.Weight); i++)
            {
                weightedList.Add(student);
            }
        }

        return weightedList;
    }
}
