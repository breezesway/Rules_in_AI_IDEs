import React from 'react';

const Wrapper = ({ children }) => (
	<div className="wrapper-outer">
		<div className="wrapper-inner">
			{children}
		</div>
	</div>
);

export default Wrapper; 