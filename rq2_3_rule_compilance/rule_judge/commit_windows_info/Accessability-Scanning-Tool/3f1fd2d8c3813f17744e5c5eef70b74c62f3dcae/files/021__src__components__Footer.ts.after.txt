export interface FooterProps {
    copyright?: string;
    compliance?: string;
}

export function renderFooter(props: FooterProps = {}): string {
    const {
        copyright = '&copy; 2024 Accessibility Testing Tool. Built with TypeScript and Node.js.',
        compliance = 'Compliant with WCAG 2.1 AAA standards'
    } = props;

    return `
        <footer class="footer">
            <div class="container">
                <p>${copyright}</p>
                <p>${compliance}</p>
            </div>
        </footer>
    `;
} 