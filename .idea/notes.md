# Datenstrukturen
- Tasks
- Semaphoren
- Mutex

# Attribute

## Task
- ID: Integer
- Task Name: String
- Aktivitäten: Aktivität[]

## Aktivität
- ID: Integer
- Name: String

## Semaphore
- ID: Integer
- Parent: Task
- Child: Task
- InitialValue: Boolean

## Mutex
- ID: Integer
- Name: String
- Tasks: Task[]
- LockedBy: Task
