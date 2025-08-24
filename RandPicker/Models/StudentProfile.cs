using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace RandPicker.Models
{
    /// <summary>
    /// 学生档案信息模型
    /// </summary>
    public class StudentProfile : INotifyPropertyChanged
    {
        private string _studentId = string.Empty;
        private string _name = string.Empty;
        private string _gender = string.Empty;
        private DateTime _birthDate = DateTime.Now;
        private string _className = string.Empty;
        private string _grade = string.Empty;
        private string _contactPhone = string.Empty;
        private string _parentName = string.Empty;
        private string _parentPhone = string.Empty;
        private string _address = string.Empty;
        private string _emergencyContact = string.Empty;
        private string _emergencyPhone = string.Empty;
        private string _remarks = string.Empty;
        private DateTime _enrollmentDate = DateTime.Now;
        private bool _isActive = true;

        public string StudentId
        {
            get => _studentId;
            set => SetProperty(ref _studentId, value);
        }

        public string Name
        {
            get => _name;
            set => SetProperty(ref _name, value);
        }

        public string Gender
        {
            get => _gender;
            set => SetProperty(ref _gender, value);
        }

        public DateTime BirthDate
        {
            get => _birthDate;
            set => SetProperty(ref _birthDate, value);
        }

        public string ClassName
        {
            get => _className;
            set => SetProperty(ref _className, value);
        }

        public string Grade
        {
            get => _grade;
            set => SetProperty(ref _grade, value);
        }

        public string ContactPhone
        {
            get => _contactPhone;
            set => SetProperty(ref _contactPhone, value);
        }

        public string ParentName
        {
            get => _parentName;
            set => SetProperty(ref _parentName, value);
        }

        public string ParentPhone
        {
            get => _parentPhone;
            set => SetProperty(ref _parentPhone, value);
        }

        public string Address
        {
            get => _address;
            set => SetProperty(ref _address, value);
        }

        public string EmergencyContact
        {
            get => _emergencyContact;
            set => SetProperty(ref _emergencyContact, value);
        }

        public string EmergencyPhone
        {
            get => _emergencyPhone;
            set => SetProperty(ref _emergencyPhone, value);
        }

        public string Remarks
        {
            get => _remarks;
            set => SetProperty(ref _remarks, value);
        }

        public DateTime EnrollmentDate
        {
            get => _enrollmentDate;
            set => SetProperty(ref _enrollmentDate, value);
        }

        public bool IsActive
        {
            get => _isActive;
            set => SetProperty(ref _isActive, value);
        }

        public int Age => DateTime.Now.Year - BirthDate.Year;

        public event PropertyChangedEventHandler? PropertyChanged;

        protected virtual void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        protected bool SetProperty<T>(ref T field, T value, [CallerMemberName] string? propertyName = null)
        {
            if (EqualityComparer<T>.Default.Equals(field, value)) return false;
            field = value;
            OnPropertyChanged(propertyName);
            return true;
        }
    }
}