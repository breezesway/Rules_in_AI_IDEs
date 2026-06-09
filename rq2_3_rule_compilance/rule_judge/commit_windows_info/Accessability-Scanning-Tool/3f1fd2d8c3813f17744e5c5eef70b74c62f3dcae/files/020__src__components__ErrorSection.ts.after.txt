export interface ErrorDetails {
    title: string;
    message: string;
    details?: string;
    actions?: {
        text: string;
        action?: string;
        class?: string;
    }[];
}

export interface ErrorSectionProps {
    error?: ErrorDetails;
    visible?: boolean;
}

export function renderErrorSection(props: ErrorSectionProps = {}): string {
    const {
        error = {
            title: 'Scan Failed',
            message: 'Unable to access the specified website. Please check the URL and try again.',
            details: 'Error Details: Connection timeout after 30 seconds',
            actions: [
                {
                    text: 'Try Again',
                    action: 'retry',
                    class: 'btn-primary'
                }
            ]
        },
        visible = false
    } = props;

    const hidden = visible ? '' : 'hidden';

    const renderActions = (actions: any[]): string => {
        if (!actions || actions.length === 0) return '';

        return `
            <div class="error-actions">
                ${actions.map(action => `
                    <button type="button" class="btn ${action.class || 'btn-primary'}" ${action.action ? `data-action="${action.action}"` : ''}>
                        <span class="btn-icon">🔄</span>
                        ${action.text}
                    </button>
                `).join('')}
            </div>
        `;
    };

    return `
        <section class="error-section" id="errorSection" aria-labelledby="error-heading" ${hidden}>
            <h2 id="error-heading" class="section-heading">Error</h2>
            <div class="error-container" id="errorContainer">
                <h3>${error.title}</h3>
                <p>${error.message}</p>
                ${error.details ? `<p><strong>Error Details:</strong> ${error.details}</p>` : ''}
                ${renderActions(error.actions || [])}
            </div>
        </section>
    `;
} 