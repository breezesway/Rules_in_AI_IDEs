import React, { useState } from 'react';
import './contact.css';

const LINKEDIN_URL = 'https://www.linkedin.com/in/josephmanghan/';

const LinkedInSVG = () => (
	<svg className="contact-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" strokeWidth="0" strokeLinecap="round" strokeLinejoin="round"><rect width="24" height="24" fill="none"/><path d="M19 0h-14c-2.76 0-5 2.24-5 5v14c0 2.76 2.24 5 5 5h14c2.76 0 5-2.24 5-5v-14c0-2.76-2.24-5-5-5zm-11 19h-3v-9h3v9zm-1.5-10.28c-.97 0-1.75-.79-1.75-1.75s.78-1.75 1.75-1.75 1.75.79 1.75 1.75-.78 1.75-1.75 1.75zm13.5 10.28h-3v-4.5c0-1.08-.02-2.47-1.5-2.47-1.5 0-1.73 1.17-1.73 2.39v4.58h-3v-9h2.89v1.23h.04c.4-.75 1.38-1.54 2.84-1.54 3.04 0 3.6 2 3.6 4.59v4.72z"/></svg>
);

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
				className="contact-link link-styling"
			>
				<LinkedInSVG />
				<span className="contact-linkedin">in/josephmanghan</span>
			</a>
		</div>
	);
};

export default Contact; 