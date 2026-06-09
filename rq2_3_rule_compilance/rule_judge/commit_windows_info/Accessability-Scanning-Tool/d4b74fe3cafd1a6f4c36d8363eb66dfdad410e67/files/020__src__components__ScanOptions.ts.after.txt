export interface ScanOption {
    id: string;
    icon: string;
    title: string;
    description: string;
    formId: string;
    inputId: string;
    inputName: string;
    inputPlaceholder: string;
    inputHelp: string;
    buttonText: string;
    buttonClass: string;
    buttonIcon: string;
}

export interface ScanOptionsProps {
    options?: ScanOption[];
}

export function renderScanOptions(props: ScanOptionsProps = {}): string {
    const defaultOptions: ScanOption[] = [
        {
            id: 'full-site',
            icon: '🌐',
            title: 'Full Site Scan',
            description: 'Comprehensive accessibility audit across your entire website (50 pages, 4 levels deep)',
            formId: 'fullSiteForm',
            inputId: 'fullSiteUrl',
            inputName: 'url',
            inputPlaceholder: 'https://example.com',
            inputHelp: 'Enter the full URL including http:// or https://',
            buttonText: 'Start Full Site Scan',
            buttonClass: 'btn-primary',
            buttonIcon: '🚀'
        },
        {
            id: 'single-page',
            icon: '📄',
            title: 'Single Page Scan',
            description: 'Quick accessibility analysis of a single web page with detailed reporting',
            formId: 'singlePageForm',
            inputId: 'singlePageUrl',
            inputName: 'url',
            inputPlaceholder: 'https://example.com/page',
            inputHelp: 'Enter the full URL of the page to test',
            buttonText: 'Start Single Page Scan',
            buttonClass: 'btn-secondary',
            buttonIcon: '📊'
        },

    ];

    const options = props.options || defaultOptions;

    const renderScanOption = (option: ScanOption): string => {

        return `
            <div class="scan-option">
                <div class="scan-option-header">
                    <span class="scan-icon">${option.icon}</span>
                    <h3>${option.title}</h3>
                </div>
                <p>${option.description}</p>
                <form class="scan-form" id="${option.formId}">
                    <div class="form-group">
                        <label for="${option.inputId}" class="form-label">${option.title} URL</label>
                        <input type="url" id="${option.inputId}" name="${option.inputName}" class="form-input"
                            placeholder="${option.inputPlaceholder}" required aria-describedby="${option.inputId}Help">
                        <div id="${option.inputId}Help" class="form-help">${option.inputHelp}</div>
                    </div>
                    <button type="submit" class="btn ${option.buttonClass}">
                        <span class="btn-icon">${option.buttonIcon}</span>
                        ${option.buttonText}
                    </button>
                </form>
            </div>
        `;
    };

    return `
        <section class="scan-section" aria-labelledby="scan-options-heading">
            <h2 id="scan-options-heading" class="section-heading">What would you like to do?</h2>
            <div class="scan-options">
                ${options.map(renderScanOption).join('')}
            </div>
        </section>
    `;
} 