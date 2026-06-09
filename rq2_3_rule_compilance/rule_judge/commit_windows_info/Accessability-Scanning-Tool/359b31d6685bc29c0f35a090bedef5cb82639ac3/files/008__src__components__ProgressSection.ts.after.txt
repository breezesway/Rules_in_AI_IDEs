export interface ProgressStage {
    id: string;
    icon: string;
    text: string;
    status?: 'pending' | 'active' | 'completed' | 'error';
}

export interface ProgressSectionProps {
    progress?: number;
    text?: string;
    details?: string;
    stages?: ProgressStage[];
    visible?: boolean;
    scanType?: 'single-page' | 'full-site';
}

export function renderProgressSection(props: ProgressSectionProps = {}): string {
    const {
        progress = 0,
        text = 'Initialising scan...',
        details = '',
        scanType = 'single-page',
        stages = scanType === 'full-site' ? [
            { id: 'init', icon: '🚀', text: 'Initialising Scan' },
            { id: 'browser-init', icon: '🌐', text: 'Browser Initialisation' },
            { id: 'crawling', icon: '🕷️', text: 'Site Crawling' },
            { id: 'analysis', icon: '🔍', text: 'Accessibility Analysis' },
            { id: 'storing', icon: '💾', text: 'Storing Results' }
        ] : [
            { id: 'init', icon: '🚀', text: 'Initialising Scan' },
            { id: 'browser-init', icon: '🌐', text: 'Browser Initialisation' },
            { id: 'analysis', icon: '🔍', text: 'Page Analysis' },
            { id: 'storing', icon: '💾', text: 'Storing Results' }
        ],
        visible = false
    } = props;

    const renderStage = (stage: ProgressStage): string => {
        const statusClass = stage.status ? ` ${stage.status}` : '';
        const statusIcon = stage.status === 'completed' ? '✅' :
            stage.status === 'active' ? '⏳' :
                stage.status === 'error' ? '❌' : stage.icon;

        return `
            <div class="stage-item${statusClass}" data-stage="${stage.id}">
                <span class="stage-icon" aria-label="${stage.text} status">${statusIcon}</span>
                <span class="stage-text">${stage.text}</span>
            </div>
        `;
    };

    return `
        <section class="progress-section" id="progressSection" aria-labelledby="progress-heading" ${visible ? '' : 'hidden'}>
            <h2 id="progress-heading" class="section-heading">Scan Progress</h2>
            <div class="progress-container">
                <div class="progress-bar" role="progressbar" aria-valuenow="${progress}" aria-valuemin="0" aria-valuemax="100" aria-label="Scan progress">
                    <div class="progress-fill" id="progressFill" style="width: ${progress}%"></div>
                </div>
                <div class="progress-text" id="progressText">${text}</div>
            </div>
            ${details ? `<div class="progress-details" id="progressDetails">${details}</div>` : ''}
            <div class="progress-stages">
                ${stages.map(renderStage).join('')}
            </div>
        </section>
    `;
} 