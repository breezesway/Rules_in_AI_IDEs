export interface HeaderProps {
    title?: string;
    subtitle?: string;
    version?: string;
}

export function renderHeader(props: HeaderProps = {}): string {
    const {
        title = 'Accessibility Testing Tool',
        subtitle = 'Professional WCAG 2.1 AAA compliance testing with comprehensive reporting',
        version = 'v2.1.1'
    } = props;

    return `
        <header class="header">
            <div class="container">
                <h1 class="logo">
                    <span class="logo-icon">🌐</span>
                    ${title}
                    <span class="version">${version}</span>
                </h1>
                <p class="tagline">${subtitle}</p>
            </div>
        </header>
    `;
} 