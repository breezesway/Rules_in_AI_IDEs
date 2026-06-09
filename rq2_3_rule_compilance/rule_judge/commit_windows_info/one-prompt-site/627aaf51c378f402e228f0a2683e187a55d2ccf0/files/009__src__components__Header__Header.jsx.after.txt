import React from 'react';
import JMLogo from '../../assets/jm_logo.webp';
import './header.css';

const Header = () => (
	<div className="header-section">
		<div className="header-content">
			<h1 className="header-title">Dr Joseph Manghan</h1>
			<img
				src={JMLogo}
				alt="Profile"
				className="header-image"
			/>
		</div>
	</div>
);

export default Header; 