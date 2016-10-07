export class Clustering{
    name: string
    method : string
    clusters: {}
    nodes= {}
}

export class Subject{
    name: string
    subject_id: string
}

export class SubjectList{
    count: number
    subjects:[Subject]
}