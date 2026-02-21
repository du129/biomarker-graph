import { useState, useEffect, useMemo } from 'react';
import { Search, ExternalLink, BookOpen } from 'lucide-react';
import { resolveCitationHref } from '../utils/citations';
import { apiUrl } from '../utils/api';

interface Citation {
    title: string;
    year: number;
    doi: string;
    type: string;
}

interface LinkData {
    source: string;
    target: string;
    summary: string;
    citations: Citation[];
}

interface NodeData {
    id: string;
    label: string;
    type: string;
}

interface PaperEntry {
    title: string;
    year: number;
    doi: string;
    type: string;
    connections: { food: string; biomarker: string; summary: string }[];
}

export default function ResearchPapers() {
    const [papers, setPapers] = useState<PaperEntry[]>([]);
    const [search, setSearch] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(apiUrl('/graph'))
            .then(res => res.json())
            .then(data => {
                const nodeMap: Record<string, string> = {};
                data.nodes.forEach((n: NodeData) => { nodeMap[n.id] = n.label; });

                const paperMap = new Map<string, PaperEntry>();
                data.links.forEach((link: LinkData) => {
                    if (!link.citations || link.citations.length === 0) return;
                    link.citations.forEach((cite: Citation) => {
                        const key = cite.doi || cite.title;
                        if (!paperMap.has(key)) {
                            paperMap.set(key, {
                                title: cite.title,
                                year: cite.year,
                                doi: cite.doi,
                                type: cite.type,
                                connections: []
                            });
                        }
                        paperMap.get(key)!.connections.push({
                            food: nodeMap[link.source] || link.source,
                            biomarker: nodeMap[link.target] || link.target,
                            summary: link.summary,
                        });
                    });
                });

                const sorted = Array.from(paperMap.values()).sort((a, b) => b.year - a.year || a.title.localeCompare(b.title));
                setPapers(sorted);
                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, []);

    const filtered = useMemo(() => {
        if (!search) return papers;
        const q = search.toLowerCase();
        return papers.filter(p =>
            p.title.toLowerCase().includes(q) ||
            p.connections.some(c => c.food.toLowerCase().includes(q) || c.biomarker.toLowerCase().includes(q) || c.summary.toLowerCase().includes(q))
        );
    }, [papers, search]);

    if (loading) {
        return <div className="page-shell"><div className="page-content text-white/50">Loading research papers...</div></div>;
    }

    return (
        <div className="page-shell">
            <div className="page-content">
                <div className="flex flex-col gap-6 mb-8">
                    <div>
                        <h1 className="text-4xl xl:text-5xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-amber-300 to-orange-400 tracking-tight mb-2">Research Papers</h1>
                        <p className="text-white/55 text-xl">
                            <span className="text-white/80 font-semibold">{papers.length}</span> cited papers backing the evidence in our database.
                        </p>
                    </div>
                    <div className="grid grid-cols-1 xl:grid-cols-[1.2fr_auto] gap-4 items-start">
                        <div className="relative w-full max-w-4xl">
                            <input
                                type="text"
                                placeholder="Search papers, foods, or biomarkers..."
                                className="toolbar-input"
                                value={search}
                                onChange={e => setSearch(e.target.value)}
                            />
                            <Search className="absolute left-4 top-4 w-5 h-5 text-white/40" />
                        </div>
                        <div className="glass-panel rounded-2xl px-5 py-3 text-sm">
                            <p className="text-white/35 uppercase text-[11px] tracking-widest">Visible Papers</p>
                            <p className="text-white text-xl font-semibold">{filtered.length}</p>
                        </div>
                    </div>
                </div>

                <div className="space-y-4">
                    {filtered.map((paper, idx) => (
                        <div key={idx} className="glass-panel rounded-2xl p-6 hover:bg-white/[0.07] transition-colors group">
                            <div className="flex items-start justify-between gap-4 mb-4">
                                <div className="flex items-start gap-3 flex-1">
                                    <div className="w-11 h-11 rounded-xl bg-amber-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <BookOpen className="w-5 h-5 text-amber-400" />
                                    </div>
                                    <div>
                                        <h3 className="font-bold text-xl text-white group-hover:text-amber-300 transition-colors leading-tight">{paper.title}</h3>
                                        <div className="flex items-center gap-3 mt-1">
                                            <span className="text-xs text-white/30 uppercase tracking-wider">{paper.type}</span>
                                            <span className="text-sm text-amber-300/80 font-semibold">{paper.year}</span>
                                        </div>
                                    </div>
                                </div>
                                {paper.doi && (
                                    <a
                                        href={resolveCitationHref(paper.doi, paper.title)}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex items-center gap-1.5 px-3 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm text-amber-200 transition-all border border-transparent hover:border-amber-500/30 flex-shrink-0"
                                    >
                                        <ExternalLink className="w-3.5 h-3.5" />
                                        <span>View Source</span>
                                    </a>
                                )}
                            </div>
                            <div className="pl-[56px] space-y-2">
                                {paper.connections.map((conn, cIdx) => (
                                    <div key={cIdx} className="flex items-center gap-2 text-base">
                                        <span className="text-blue-300 font-medium">{conn.food}</span>
                                        <span className="text-white/20">→</span>
                                        <span className="text-pink-300 font-medium">{conn.biomarker}</span>
                                        <span className="text-white/35 text-sm hidden xl:inline">— {conn.summary}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>

                {filtered.length === 0 && (
                    <div className="text-center py-20 text-white/30">
                        <p className="text-xl">No papers match your search.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
