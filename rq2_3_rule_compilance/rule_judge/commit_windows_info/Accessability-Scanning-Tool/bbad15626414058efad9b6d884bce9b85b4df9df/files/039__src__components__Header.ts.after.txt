export interface HeaderProps {
    title?: string;
    subtitle?: string;
    version?: string;
    currentPage?: 'home' | 'single-page' | 'full-site' | 'reports';
}

export function renderHeader(props: HeaderProps = {}): string {
    const {
        title = 'Accessibility Testing Tool',
        subtitle = 'Professional WCAG 2.1 AAA compliance testing with comprehensive reporting',
        version = 'v2.1.1',
        currentPage = 'home'
    } = props;

    const navItems = [
        { href: '/', label: 'Home', icon: '🏠' },
        { href: '/single-page', label: 'Single Page Scan', icon: '📄' },
        { href: '/full-site', label: 'Full Site Scan', icon: '🌐' },
        { href: '/reports', label: 'Search Reports', icon: '📊' }
    ];

    const navHtml = navItems.map(item => {
        const isActive = (currentPage === 'home' && item.href === '/') || 
                        (currentPage !== 'home' && item.href.includes(currentPage));
        return `
            <a href="${item.href}" class="nav-link ${isActive ? 'active' : ''}" aria-current="${isActive ? 'page' : 'false'}">
                <span class="nav-icon">${item.icon}</span>
                ${item.label}
            </a>
        `;
    }).join('');

    return `
        <header class="header">
            <div class="container">
                <div class="header-content">
                    <h1 class="logo">
                        <span class="logo-icon">🌐</span>
                        ${title}
                        <span class="version">${version}</span>
                    </h1>
                    <p class="tagline">${subtitle}</p>
                </div>
                <nav class="main-nav" aria-label="Main navigation">
                    ${navHtml}
                </nav>
            </div>
        </header>
    `;
} 