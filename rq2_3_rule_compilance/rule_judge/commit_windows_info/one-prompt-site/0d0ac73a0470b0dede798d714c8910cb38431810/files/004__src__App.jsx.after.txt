import React from 'react';
import Wrapper from './components/Wrapper/Wrapper';
import Header from './components/Header/Header';
import Bio from './components/Bio/Bio';
import Contact from './components/Contact/Contact';
import Blog from './components/Blog';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/one-prompt-site-blog" element={<Blog />} />
				<Route path="/*" element={
					<Wrapper>
						<Header />
						<Bio />
						<Contact />
					</Wrapper>
				} />
			</Routes>
		</Router>
	);
}

export default App;
