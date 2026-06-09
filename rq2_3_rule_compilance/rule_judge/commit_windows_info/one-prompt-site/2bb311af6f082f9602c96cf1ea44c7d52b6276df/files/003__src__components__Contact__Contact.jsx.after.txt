import React, { useState } from 'react';

const LINKEDIN_URL = 'https://www.linkedin.com/in/josephmanghan/';

const Contact = () => {
	const [copied, setCopied] = useState(false);
	const handleCopy = () => {
		navigator.clipboard.writeText('josephmanghan@gmail.com');
		setCopied(true);
		setTimeout(() => setCopied(false), 1800);
	};
	return (
		<div className="contact-section">
			<button
				onClick={handleCopy}
				className="contact-btn"
				aria-label="Copy email address"
			>
				<span className="material-icons contact-icon">mail</span>
				<span className="contact-email">josephmanghan@gmail.com</span>
				{copied && (
					<span className="contact-copied">Copied!</span>
				)}
			</button>
			<a
				href={LINKEDIN_URL}
				target="_blank"
				rel="noopener noreferrer"
				className="contact-link"
			>
				<span className="material-icons contact-icon">linkedin</span>
				<span className="contact-linkedin">in/josephmanghan</span>
			</a>
		</div>
	);
};

export default Contact; 