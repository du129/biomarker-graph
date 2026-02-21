export interface Node {
    id: string;
    label: string;
    type: 'food' | 'biomarker';
    group: string;
    image?: string;
    target?: string;
    description?: string;
    val?: number;
}

export interface Link {
    source: string;
    target: string;
    effect: 'increase' | 'decrease';
    strength: 'high' | 'medium' | 'low';
    magnitude: string;
    timeframe: string;
    summary: string;
    citations: Citation[];
}

export interface Citation {
    title: string;
    year: number;
    doi: string;
    type: string;
}

export interface GraphData {
    nodes: Node[];
    links: Link[];
}
