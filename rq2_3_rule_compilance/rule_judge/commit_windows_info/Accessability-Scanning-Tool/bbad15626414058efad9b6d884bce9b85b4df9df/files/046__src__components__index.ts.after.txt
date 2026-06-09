// Main WebInterface component
export { renderWebInterface, WebInterfaceProps } from './WebInterface';

// Page components
export { renderLandingPage, LandingPageProps } from './LandingPage';
export { renderSinglePageScanPage, SinglePageScanPageProps } from './SinglePageScanPage';
export { renderFullSiteScanPage, FullSiteScanPageProps } from './FullSiteScanPage';
export { renderReportsPage, ReportsPageProps } from './ReportsPage';

// Individual components
export { renderHeader, HeaderProps } from './Header';
export { renderScanOptions, ScanOptionsProps, ScanOption } from './ScanOptions';
export { renderProgressSection, ProgressSectionProps, ProgressStage } from './ProgressSection';
export { renderResultsSection, ResultsSectionProps, ScanResult } from './ResultsSection';
export { renderErrorSection, ErrorSectionProps, ErrorDetails } from './ErrorSection';
export { renderFooter, FooterProps } from './Footer'; 