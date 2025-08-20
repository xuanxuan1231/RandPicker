using System;
using System.Collections.Generic;
using System.IO;
using RandPicker.Models;
using Serilog;

namespace RandPicker.ViewModels;

public class MainWindowViewModel : ViewModelBase
{
    private List<Student> _students = new();
    private readonly Random _random = new();

    private string _resultName = "无结果";
    private string _resultId = "000000";

    public string ResultName
    {
        get => _resultName;
        set
        {
            _resultName = value;
            OnPropertyChanged();
        }
    }

    public string ResultId
    {
        get => _resultId;
        set
        {
            _resultId = value;
            OnPropertyChanged();
        }
    }

    public MainWindowViewModel()
    {
        LoadStudents();
    }


    private void LoadStudents()
    {
        // 密码的 BaseDirectory
        var dir = Path.GetDirectoryName(Environment.ProcessPath) ?? AppDomain.CurrentDomain.BaseDirectory;
        var jsonPath = Path.Combine(dir, "students.json");
        _students = StudentService.LoadFromJson(jsonPath);
    }

    public void PickPerson()
    {
        // 刷新学生数据
        LoadStudents();

        // 获取活跃的学生
        var activeStudents = StudentService.GetActiveList(_students);

        // 一个都没有
        if (activeStudents.Count == 0)
        {
            ResultName = "无结果";
            ResultId = "000000";
            Log.Warning("没有启用的学生。");
            return;
        }

        // 加权 随机
        var weightedStudents = StudentService.GetWeightedList(activeStudents);
        var selectedStudent = weightedStudents[_random.Next(weightedStudents.Count)];

        ResultName = selectedStudent.Name;
        ResultId = selectedStudent.Id.ToString();

        Log.Information($"选中: {selectedStudent.Name} (ID: {selectedStudent.Id})");
    }
}