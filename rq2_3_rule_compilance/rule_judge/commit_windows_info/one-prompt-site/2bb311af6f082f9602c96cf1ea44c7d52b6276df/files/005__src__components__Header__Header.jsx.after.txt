import React from 'react';
import JMLogo from '../../assets/JM_logo.png';

const Header = () => (
	<div className="header-section">
		<div>
			<h1 className="header-title">Dr Joe Manghan</h1>
		</div>
		<div>
			<img
				src={JMLogo}
				alt="Profile"
				className="header-image"
			/>
		</div>
	</div>
);

export default Header; 