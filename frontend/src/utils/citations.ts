const DOI_PATTERN = /^10\.\S+\/\S+$/i;
const DOI_URL_PATTERN = /^(https?:\/\/)?(dx\.)?doi\.org\/10\.\S+\/\S+$/i;

export function resolveCitationHref(rawDoi?: string, title?: string): string {
    const raw = (rawDoi || '').trim();

    if (raw) {
        if (/^https?:\/\//i.test(raw)) return raw;

        const pmidMatch = raw.match(/^pmid:\s*(\d+)$/i);
        if (pmidMatch) return `https://pubmed.ncbi.nlm.nih.gov/${pmidMatch[1]}/`;

        if (DOI_URL_PATTERN.test(raw)) return raw.startsWith('http') ? raw : `https://${raw}`;
        if (DOI_PATTERN.test(raw)) return `https://doi.org/${raw}`;

        return `https://pubmed.ncbi.nlm.nih.gov/?term=${encodeURIComponent(raw)}`;
    }

    if (title && title.trim()) {
        return `https://pubmed.ncbi.nlm.nih.gov/?term=${encodeURIComponent(title.trim())}`;
    }

    return 'https://pubmed.ncbi.nlm.nih.gov/';
}
