# GUID 功能说明

## 概述

RandPicker 使用 GUID (Globally Unique Identifier) 作为学生的唯一标识符，用于支持高级抽选功能。每个学生都有一个唯一的 GUID，通过 `uuid.uuid4()` 生成。

## 数据结构

学生数据包含以下字段：

```json
{
  "guid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "张三",
  "weight": 1,
  "enabled": true,
  "avatar": "",
  "properties": []
}
```

- `guid`: 学生的唯一标识符（UUID v4 格式）
- `name`: 学生姓名
- `weight`: 抽选权重
- `enabled`: 是否启用该学生
- `avatar`: 头像路径
- `properties`: 附加属性列表

## 核心实现

### 1. 自动生成 GUID

当添加新学生时，系统会自动生成一个唯一的 GUID：

```python
@Slot(str, int, bool)
def add_student(self, name: str, weight: int = 1, enabled: bool = True) -> None:
    new_student = {
        "guid": str(uuid.uuid4()),  # 自动生成 GUID
        "name": name,
        "weight": weight,
        "enabled": enabled
    }
    self.config["students"].append(new_student)
```

### 2. 使用 GUID 进行抽选

抽选功能现在使用 GUID 而不是索引：

```python
def _refresh(self):
    students = self.studentsConfig.get_students()
    self.students = []
    self.students_weights = []
    for student in students:
        if student.get("enabled", False):
            self.students.append(student.get("guid"))  # 收集 GUID
            self.students_weights.append(student.get("weight", 1))
```

### 3. 通过 GUID 查找学生信息

抽选结果通过 GUID 查找对应的学生信息：

```python
students_list = self.studentsConfig.get_students()
for guid in result:
    for student in students_list:
        if student.get("guid") == guid:
            student_copy = student.copy()
            student_copy["properties"] = student.get("properties", [])
            student_copy["avatar"] = student.get("avatar", "")
            final_result.append(student_copy)
            break
```

## 未来扩展

GUID 功能为以下高级功能奠定基础：

- 基于附加属性的筛选抽选
- 学生分组管理
- 抽选历史记录
- 跨设备数据同步