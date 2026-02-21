import type { Node } from '../types';
import { X, Search, ExternalLink } from 'lucide-react';
import { useState, useMemo, useEffect, useRef } from 'react';
import { resolveCitationHref } from '../utils/citations';

interface HUDProps {
    selectedNode: Node | null;
    selectedLinks: any[];
    onClose: () => void;
    onSearch: (query: string) => void;
    graphData: { nodes: Node[] };
}

export function HUD({ selectedNode, selectedLinks, onClose, onSearch, graphData }: HUDProps) {
    const [searchQuery, setSearchQuery] = useState('');
    const [showSearchResults, setShowSearchResults] = useState(false);
    const searchInputRef = useRef<HTMLInputElement>(null);

    const searchResults = useMemo(() => {
        if (!searchQuery) return [];
        return graphData.nodes.filter(n => n.label.toLowerCase().includes(searchQuery.toLowerCase())).slice(0, 12);
    }, [searchQuery, graphData.nodes]);

    const highStrengthCount = useMemo(
        () => selectedLinks.filter((link: any) => link.strength === 'high').length,
        [selectedLinks]
    );

    useEffect(() => {
        const handler = (event: KeyboardEvent) => {
            const target = event.target as HTMLElement | null;
            const targetTag = target?.tagName.toLowerCase();
            const typingInInput = targetTag === 'input' || targetTag === 'textarea' || target?.isContentEditable;
            if (!typingInInput && event.key === '/') {
                event.preventDefault();
                searchInputRef.current?.focus();
            }
            if (event.key === 'Escape') {
                setShowSearchResults(false);
                if (selectedNode) onClose();
            }
        };
        window.addEventListener('keydown', handler);
        return () => window.removeEventListener('keydown', handler);
    }, [selectedNode, onClose]);

    const handleSearchSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSearch(searchQuery);
        setShowSearchResults(false);
    };

    return (
        <>
            {/* ── Search Bar — top center ──────────────────────── */}
            <div className="absolute top-3 md:top-5 left-1/2 -translate-x-1/2 z-20 w-[min(620px,calc(100vw-1rem))] pointer-events-auto">
                <form onSubmit={handleSearchSubmit} className="relative group">
                    <div className="absolute inset-0 bg-blue-500/15 rounded-2xl blur-lg opacity-0 group-hover:opacity-100 transition-opacity" />
                    <input
                        ref={searchInputRef}
                        type="text"
                        placeholder="Search foods or biomarkers…"
                        className="relative w-full glass-panel-strong rounded-2xl py-3 px-11 pr-20 text-base text-white placeholder-white/35 focus:outline-none focus:border-blue-500/40 focus:ring-1 focus:ring-blue-500/30 transition-all shadow-lg"
                        value={searchQuery}
                        onChange={(e) => {
                            setSearchQuery(e.target.value);
                            setShowSearchResults(true);
                        }}
                        onFocus={() => setShowSearchResults(true)}
                    />
                    <Search className="absolute left-4 top-3.5 w-4 h-4 text-white/45" />
                    <span className="absolute right-4 top-3 text-xs px-2 py-1 rounded-md border border-white/10 text-white/55 bg-black/40">/</span>
                </form>

                {/* Dropdown */}
                {showSearchResults && searchQuery && (
                    <div className="absolute top-12 left-0 w-full glass-panel rounded-2xl overflow-hidden max-h-[320px] overflow-y-auto">
                        <div className="px-4 py-2.5 border-b border-white/10 text-sm text-white/60">
                            {searchResults.length} result{searchResults.length !== 1 ? 's' : ''}
                        </div>
                        {searchResults.length > 0 ? (
                            searchResults.map(node => (
                                <div
                                    key={node.id}
                                    className="px-4 py-3 hover:bg-white/10 cursor-pointer flex items-center gap-3 border-b border-white/5 last:border-0 transition-colors"
                                    onClick={() => {
                                        onSearch(node.label);
                                        setSearchQuery(node.label);
                                        setShowSearchResults(false);
                                    }}
                                >
                                    <div className={`w-2 h-2 rounded-full ${node.type === 'food' ? 'bg-blue-400' : 'bg-red-400'}`} />
                                    <span className="font-medium text-white/85 text-base">{node.label}</span>
                                    <span className="text-sm text-white/40 ml-auto uppercase tracking-wider">{node.group}</span>
                                </div>
                            ))
                        ) : (
                            <div className="px-4 py-4 text-white/30 text-sm text-center">No results found. Try a food group or biomarker family.</div>
                        )}
                    </div>
                )}
            </div>

            {/* ── Detail Panel — right side ────────────────────── */}
            {selectedNode && (
                <div className="absolute top-2 left-2 right-2 z-20 h-[calc(100%-16px)] pointer-events-auto overflow-y-auto hide-scrollbar md:top-4 md:left-auto md:right-4 md:w-[440px] md:max-w-[calc(100vw-380px)] md:h-[calc(100%-32px)]">
                    <div className="glass-panel-strong rounded-2xl p-5 float-up">

                        {/* Header */}
                        <div className="flex justify-between items-start mb-4 pb-4 border-b border-white/8">
                            <div className="flex-1">
                                <div className="flex items-center gap-2 mb-1.5">
                                    <span className={`w-2 h-2 rounded-full ${selectedNode.type === 'food' ? 'bg-blue-400' : 'bg-red-400'}`} />
                                    <span className={`text-sm uppercase tracking-wider font-bold ${selectedNode.type === 'food' ? 'text-blue-300' : 'text-red-300'}`}>
                                        {selectedNode.type}
                                    </span>
                                </div>
                                <h2 className="text-2xl font-extrabold text-white tracking-tight">{selectedNode.label}</h2>
                                <p className="text-white/60 text-base font-medium mt-0.5">{selectedNode.group}</p>
                            </div>
                            <button
                                onClick={onClose}
                                className="h-11 w-11 bg-white/5 hover:bg-white/15 rounded-lg transition-all flex items-center justify-center"
                            >
                                <X className="w-4 h-4 text-white/50 hover:text-white" />
                            </button>
                        </div>

                        <div className="grid grid-cols-2 gap-2 mb-4">
                            <div className="rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2.5">
                                <p className="text-xs uppercase tracking-wider text-white/55">Linked studies</p>
                                <p className="text-lg font-bold text-white">{selectedLinks.length}</p>
                            </div>
                            <div className="rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2.5">
                                <p className="text-xs uppercase tracking-wider text-white/55">High-strength</p>
                                <p className="text-lg font-bold text-emerald-300">{highStrengthCount}</p>
                            </div>
                        </div>

                        {selectedNode.description && (
                            <div className="mb-5 p-3 bg-white/[0.03] rounded-xl border border-white/5">
                                <p className="text-sm text-gray-300 leading-relaxed">{selectedNode.description}</p>
                            </div>
                        )}

                        {/* Relationships */}
                        <div className="space-y-3">
                            <h3 className="text-sm font-bold text-white/50 uppercase tracking-wider mb-3">
                                {selectedNode.type === 'food' ? 'Proven Health Benefits' : 'Dietary Interventions'}
                                <span className="ml-2 font-mono text-white/15">{selectedLinks.length}</span>
                            </h3>

                            {selectedLinks.length === 0 ? (
                                <div className="text-center py-6 bg-white/[0.02] rounded-xl border border-dashed border-white/8">
                                    <p className="text-base text-white/45">No linked evidence.</p>
                                </div>
                            ) : (
                                selectedLinks.map((link, idx) => {
                                    const connectedNodeId = (typeof link.source === 'object' ? link.source.id : link.source) === selectedNode.id
                                        ? (typeof link.target === 'object' ? link.target.id : link.target)
                                        : (typeof link.source === 'object' ? link.source.id : link.source);

                                    const connectedNode = graphData.nodes.find(n => n.id === connectedNodeId);

                                    const isImprovement = (link.effect === 'decrease' && (connectedNode?.label.includes('LDL') || connectedNode?.label.includes('Triglycerides') || connectedNode?.label.includes('BP') || connectedNode?.label.includes('CRP')))
                                        || link.effect === 'increase';

                                    return (
                                        <div
                                            key={idx}
                                            className={`rounded-xl p-4 border transition-all duration-200 ${isImprovement
                                                ? 'bg-gradient-to-br from-green-500/[0.04] to-emerald-900/[0.06] border-green-500/15 hover:border-green-400/30'
                                                : 'bg-gradient-to-br from-blue-500/[0.04] to-indigo-900/[0.06] border-blue-500/15 hover:border-blue-400/30'
                                                }`}
                                        >
                                            <div className="flex items-center justify-between mb-2">
                                                <span className="font-bold text-white text-base">{connectedNode?.label}</span>
                                                <span className={`text-xs font-black tracking-wider px-1.5 py-0.5 rounded-md ${link.strength === 'high' ? 'bg-green-500/20 text-green-400' : link.strength === 'medium' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-white/10 text-white/40'}`}>
                                                    {link.strength.toUpperCase()}
                                                </span>
                                            </div>

                                            <div className="text-sm text-white/70 font-medium mb-2 flex items-baseline gap-1.5">
                                                {link.effect === 'decrease' ? 'Reduces' : 'Increases'} by
                                                <span className={`text-base font-bold ${isImprovement ? 'text-green-400' : 'text-blue-400'}`}>{link.magnitude}</span>
                                            </div>

                                            <p className="text-sm text-gray-400 mb-3 leading-relaxed pl-2.5 border-l-2 border-white/8 italic">
                                                "{link.summary}"
                                            </p>

                                            <div className="flex items-center justify-between pt-2 border-t border-white/5">
                                                <span className="text-xs text-white/35 font-mono">{link.timeframe}</span>
                                                {link.citations && link.citations.length > 0 && (
                                                    <div className="flex gap-1.5">
                                                        {link.citations.map((cite: any, cIdx: number) => (
                                                            <a
                                                                key={cIdx}
                                                                href={resolveCitationHref(cite.doi, cite.title)}
                                                                target="_blank"
                                                                rel="noopener noreferrer"
                                                                className="flex items-center gap-1 px-2 py-1 bg-white/[0.04] hover:bg-white/[0.08] rounded-md text-sm text-blue-300 transition-all border border-transparent hover:border-blue-500/20"
                                                                title={`${cite.title} (${cite.year})`}
                                                            >
                                                                <ExternalLink className="w-2.5 h-2.5" />
                                                                <span>Ref {cIdx + 1}</span>
                                                            </a>
                                                        ))}
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    );
                                })
                            )}
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
