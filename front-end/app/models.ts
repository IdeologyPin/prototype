export class Clustering{
    name: string
    method : string
    clusters: {}
    nodes= {}
}

export class Subject{
    _id:number
    name: string
    children:[number]
}

export class SubjectList{
    count: number
    subjects:[Subject]
}