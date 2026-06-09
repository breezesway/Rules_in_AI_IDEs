import React from 'react';
import Wrapper from './components/Wrapper/Wrapper';
import Header from './components/Header/Header';
import Bio from './components/Bio/Bio';
import Contact from './components/Contact/Contact';

function App() {
	return (
		<Wrapper>
			<Header />
			<Bio />
			<Contact />
		</Wrapper>
	);
}

export default App;
