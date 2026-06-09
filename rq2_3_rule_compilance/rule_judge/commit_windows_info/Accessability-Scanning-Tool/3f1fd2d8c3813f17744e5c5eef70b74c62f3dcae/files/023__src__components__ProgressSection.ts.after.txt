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
}

export function renderProgressSection(props: ProgressSectionProps = {}): string {
    const {
        progress = 0,
        text = 'Initialising scan...',
        details = '',
        stages = [
            { id: 'browser', icon: '🌐', text: 'Browser Initialisation' },
            { id: 'navigation', icon: '🧭', text: 'Website Navigation' },
            { id: 'axe', icon: '🔍', text: 'Axe-Core Analysis' },
            { id: 'pa11y', icon: '📊', text: 'Pa11y Analysis' },
            { id: 'processing', icon: '⚙️', text: 'Processing Results' },
            { id: 'reports', icon: '📄', text: 'Generating Reports' }
        ],
        visible = false
    } = props;

    const hidden = visible ? '' : 'hidden';

    const renderStage = (stage: ProgressStage): string => {
        const statusClass = stage.status ? ` ${stage.status}` : '';
        return `
            <div class="stage-item${statusClass}" data-stage="${stage.id}">
                <span class="stage-icon">${stage.icon}</span>
                <span class="stage-text">${stage.text}</span>
            </div>
        `;
    };

    return `
        <section class="progress-section" id="progressSection" aria-labelledby="progress-heading" ${hidden}>
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