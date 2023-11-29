import React from 'react';
import styled from 'styled-components';
import { useState } from 'react';
const Container = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(to right, #003366, #004080, #0059b3, #0073e6);
`;
const Wrapper = styled.div`
  overflow: hidden;
  max-width: 390px;
  background: #fff;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0px 15px 20px rgba(0, 0, 0, 0.1);
  
`;

const TitleText = styled.div`
  display: flex;
  width: 200%;
`;

const Title = styled.div`
  width: 50%;
  font-size: 35px;
  font-weight: 600;
  text-align: center;
  transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);

  &:first-child {
    margin-left: ${(props) => (props.state=='login' ? "-50%" : "0%")};
  }
`;

const SlideControls = styled.div`
  position: relative;
  display: flex;
  height: 50px;
  width: 100%;
  overflow: hidden;
  margin: 30px 0 10px 0;
  justify-content: space-between;
  border: 1px solid lightgrey;
  border-radius: 15px;
`;

const Slide = styled.label`
  height: 100%;
  width: 100%;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  line-height: 48px;
  cursor: pointer;
  z-index: 1;
  transition: all 0.6s ease;
  &:last-child {
    color: #000;
  }
  color:${(props) => props.state=='login'?'white': 'black'};
`;

const SliderTab = styled.div`
  position: absolute;
  height: 100%;
  width: 50%;
  left: 0;
  z-index: 0;
  border-radius: 15px;
  transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  background: -webkit-linear-gradient(left, #003366,#004080,#0059b3
    , #0073e6);
  ${(props) => props.state!='login' && 'left: 50%'};
`;

const FormContainer = styled.div`
  width: 100%;
  overflow: hidden;
`;

const FormInner = styled.div`
  display: flex;
  width: 200%;
`;

const Form = styled.form`
  width: 50%;
  transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  &:first-child {
    margin-left: ${(props) => (props.state!='login' ? "-50%" : "0%")};
  }
`;

const Field = styled.div`
  height: 50px;
  width: 100%;
  margin-top: 20px;
  border:0px;
`;

const Input = styled.input`
  height: 100%;
  width: 100%;
  outline: none;
  padding-left: 15px;
  border-radius: 15px;
  border: 1px solid lightgrey;
  border-bottom-width: 2px;
  font-size: 17px;
  transition: all 0.3s ease;

  &:focus {
    border-color: #1a75ff;
  }

  &::placeholder {
    color: #999;
    transition: all 0.3s ease;
  }

  &:focus::placeholder {
    color: #1a75ff;
  }
`;

const PassLink = styled.div`
  margin-top: 5px;
`;

const SignupLink = styled.div`
  text-align: center;
  margin-top: 30px;
`;

const Btn = styled.div`
  height: 50px;
  width: 100%;
  position: relative;
  overflow: hidden;
`;

const BtnLayer = styled.div`
  height: 100%;
  width: 300%;
  position: absolute;
  left: -100%;
  background: linear-gradient(right, #003366, #004080, #0059b3, #0073e6);
  border-radius: 15px;
  transition: all 0.4s ease;
   
  ${Btn}:hover & {
    left: 0;
  }
`;
const Link=styled.text`
color: #1a75ff;
cursor:pointer;
text-decoration:underline;
`
const BtnInput = styled.button`
  height: 100%;
  width: 100%;
  z-index: 1;
  position: relative;
  background: -webkit-linear-gradient(left, #003366,#004080,#0059b3
    , #0073e6);
  color: #fff;
  padding-left: 0;
  border-radius: 15px;
  font-size: 17px;
  font-weight: bold;
  cursor: pointer;
`;

const Auth = () => {
  const [authState, setAuthState] = useState('login');

  const handleSignupClick = () => {
    setAuthState('signup')
  };

  const handleLoginClick = () => {
    setAuthState('login')
  };
  return (
    <Container>
    <Wrapper>
      <TitleText>
        <Title state={authState}>SignUp Form</Title>
        <Title state={authState}>Login Form</Title>
      </TitleText>
      <SlideControls>
        <Slide state={authState} onClick={handleLoginClick}>
          Login
        </Slide>
        <Slide state={authState=='login'?'signup':'login'} onClick={handleSignupClick}>
          Signup
        </Slide>
        <SliderTab state={authState} />
      </SlideControls>
      <FormContainer>
        <FormInner>
          <Form action="#" className="login" state={authState}>
            <Field>
              <Input type="text" placeholder="Email Address" required />
            </Field>
            <Field>
              <Input type="password" placeholder="Password" required />
            </Field>
            <PassLink>
              <Link >Forgot password?</Link>
            </PassLink>
            <Field className="btn">
              <Btn>
                <BtnLayer />
                <BtnInput type="submit">Login</BtnInput>
              </Btn>
            </Field>
            <SignupLink>
              Not a member? <Link >Signup now</Link>
            </SignupLink>
          </Form>
          <Form action="#" className="signup" state={authState}>
            <Field>
              <Input type="text" placeholder="Email Address" required />
            </Field>
            <Field>
              <Input type="password" placeholder="Password" required />
            </Field>
            <Field>
              <Input type="password" placeholder="Confirm password" required />
            </Field>
            <Field className="btn">
              <Btn>
                <BtnLayer />
                <BtnInput type="submit">Signup</BtnInput>
              </Btn>
            </Field>
          </Form>
        </FormInner>
      </FormContainer>
    </Wrapper>
    </Container>
  );
};

export default Auth;
