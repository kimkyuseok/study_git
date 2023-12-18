ShotGrid API에서 `filters`와 `fields`는 데이터를 검색하고 반환하는 데 사용되는 중요한 매개변수입니다.

1. **Filters (필터):**
   - `filters`는 데이터를 검색할 때 적용되는 조건을 정의하는 데 사용됩니다.
   - 예를 들어, 특정 프로젝트의 특정 태스크 유형에 속하는 작업만 검색하려면 다음과 같은 필터를 사용할 수 있습니다:

     ```python
     filters = [
         {'filter_operator': 'all',
          'filters': [
              ['project', 'is', {'type': 'Project', 'id': project_id}],
              ['task', 'type', 'is', 'Task'],
              ['task', 'sg_task_type', 'is', 'Animation']
          ]}
     ]
     ```

     이 예제에서는 특정 프로젝트 ID에 속하며 태스크 유형이 "Animation"인 모든 작업을 검색하는 필터를 정의합니다.

2. **Fields (필드):**
   - `fields`는 반환되는 데이터에 포함되어야 하는 필드를 지정하는 데 사용됩니다.
   - 원하는 필드만 가져와서 응답의 크기를 최적화할 수 있습니다.
   - 예를 들어, 작업의 ID, 이름 및 상태만 필요한 경우 다음과 같이 `fields`를 사용할 수 있습니다:

     ```python
     fields = ['id', 'content', 'sg_status_list']
     ```

     이렇게 하면 작업의 ID, 내용 및 상태만을 포함하는 결과가 반환됩니다.

조합해서 사용하는 경우, 예를 들면:

```python
filters = [
    {'filter_operator': 'all',
     'filters': [
         ['project', 'is', {'type': 'Project', 'id': project_id}],
         ['task', 'type', 'is', 'Task'],
         ['task', 'sg_task_type', 'is', 'Animation']
     ]}
]

fields = ['id', 'content', 'sg_status_list']

tasks = sg.find('Task', filters, fields)
```

위의 예제에서는 특정 프로젝트에 속하며 태스크 유형이 "Animation"인 작업 중 ID, 내용 및 상태만을 가져오는 방법을 보여줍니다.
