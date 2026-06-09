import React from 'react';
import './bio.css';

const LINKEDIN_URL = 'https://www.linkedin.com/in/josephmanghan/';
const PHD_URL = 'https://eprints.soton.ac.uk/443879/#:~:text=Manghan%2C%20Joseph%20Philip%20(2020),%2C%20Doctoral%20Thesis%2C%20237pp.';

const Bio = () => (
	<div className="bio-section">
		<p>
			I'm Joe – a <a
				href={LINKEDIN_URL}
				className="link-styling"
				target="_blank"
				rel="noopener noreferrer"
			>Frontend Developer</a> who enjoys writing clean, scalable code, and thoughtful UX. I work on authentication and identity solutions within digital banking.
		</p>
		<p>
			Right now I'm focused on the evolving AI discourse and exploring how AI can be meaningfully integrated into both product and workflow contexts.
		</p>
		<p>
			Beyond development, I enjoy weightlifting, long walks, art, and the odd video game. I hold a <a
				href={PHD_URL}
				className="link-styling"
				target="_blank"
				rel="noopener noreferrer"
			>PhD</a> that explored using web practices to outsource compositional tasks to crowds.
		</p>
	</div>
);

export default Bio; 