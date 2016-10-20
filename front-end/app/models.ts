export class Node{
    article: String
    span_type: String
    label: String
    vector: number[]
    scores: Map<String, number>

}

export class Cluster{
    id:string
    name: string
    tags: string[]
    vector: number[]
    nodes: Node[]

}

export class Clustering{
    id: number
    name: string
    method : string
    clusters: Cluster[]
    nodes: Node[]
}

export class ClusteringList{
    clusterings: Clustering[]
}


export class Subject{
    _id:number
    name: string
    children:[number]
}

export class SubjectList{
    count: number
    subjects:Subject[]
}