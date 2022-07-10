import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { Panel, PanelHeader, List,  Input, Button, Group, Cell, Div, Avatar, Tabs, HorizontalScroll, TabsItem, CellButton } from '@vkontakte/vkui';
import axios from 'axios'
import bridge from "@vkontakte/vk-bridge";
const Home = ({ id, go, fetchedUser }) => {
	const [state, setState] = useState('text')
	const [imageuri, setImage] = useState()
	const [dataImage, setDataImage] = useState([])
	const textInput = React.createRef();
	const changeStatuses = (status) => {
		setState(status)
	}
	
	const makeStory = (image) => {
		bridge.send("VKWebAppShowStoryBox", { "background_type" : "image", "url" : image });
	}

	const getPhoto = () => {
		axios.get(`https://aca1-92-38-163-23.ngrok.io/images`)
			.then(el => el.data)
			.then(el => setDataImage(el))
		console.log(dataImage)
	}

	useEffect(() => {
		getPhoto()
	}, [])

	const makePrint = async () => {
		var c = document.getElementById("textCanvas");
		var ctx = c.getContext("2d");

		ctx.font = "20px Georgia";
		ctx.fillText(`@${fetchedUser?.first_name}`, 10, 30);

		ctx.font = "30px Verdana";
		// Create gradient
		var gradient = ctx.createLinearGradient(0, 0, c.width, 0);
		gradient.addColorStop("0"," magenta");
		gradient.addColorStop("0.5", "blue");
		gradient.addColorStop("1.0", "red");
		// Fill with gradient
		ctx.fillStyle = gradient;
		ctx.fillText(textInput?.current?.value, 10, 70);
		axios.post(`https://aca1-92-38-163-23.ngrok.io/images`, {
			user: fetchedUser,
			img:  ctx.canvas.toDataURL()
		})
	}
	return (
		<Panel id={id}>
			<PanelHeader>Example</PanelHeader>
			    <Group>
					<Tabs>
						<HorizontalScroll>
							<TabsItem
								onClick={() =>changeStatuses('text')}
								selected={state === "text"}
							>
								Афтограф текстом
							</TabsItem>
							<TabsItem
							onClick={() => { changeStatuses('show'); getPhoto(); }}
								selected={state === "show"}
							>
								Посмотрить автографы
							</TabsItem>
							<TabsItem
								onClick={() => changeStatuses('draw')}
								selected={state === "draw"}
							>
								Нарисовать автограф
							</TabsItem>
						</HorizontalScroll>
					</Tabs>
				</Group>
			{/* {fetchedUser &&
				<Group header={<Header mode="secondary">User Data Fetched with VK Bridge</Header>}>
					<Cell
						before={fetchedUser.photo_200 ? <Avatar src={fetchedUser.photo_200} /> : null}
						description={fetchedUser.city && fetchedUser.city.title ? fetchedUser.city.title : ''}
					>
						{`${fetchedUser.first_name} ${fetchedUser.last_name}`}
					</Cell>
				</Group>} */}
			{state === 'text' && (
				<>
				<Group>
					<Div>
						<Input type="text" getRef={textInput} />
					</Div>
					<Div>
						<Button onClick={makePrint}>Создать</Button>
					</Div>
				</Group>
				<Group>
						<Div>
							<canvas id='textCanvas'></canvas>
							<img id='image' style={{display: 'none'}} />
						</Div>
				</Group>
				</>
			)}
			{state === 'show' && (
				<>
					<Group>
						<List>
							{dataImage ? dataImage.map(el => {
								return (
									<Cell expandable
										before={
											<img src={el.img} />
										}
										after={
											<>
												<Avatar src={el?.user?.photo_200} />
												{fetchedUser?.id === el?.user?.id && (<Button onClick={() => makeStory(el?.img)}>Опубликовать в историю</Button>)}
											</>
										}
									>
										Автор - {el?.user?.last_name} {el?.user?.first_name}
									</Cell>)
							}) : ''}
						</List>
				</Group>
				</>
			)}
			<Group>
			</Group>
		</Panel>
	)
}
Home.propTypes = {
	id: PropTypes.string.isRequired,
	go: PropTypes.func.isRequired,
	fetchedUser: PropTypes.shape({
		photo_200: PropTypes.string,
		first_name: PropTypes.string,
		last_name: PropTypes.string,
		city: PropTypes.shape({
			title: PropTypes.string,
		}),
	}),
};

export default Home;
