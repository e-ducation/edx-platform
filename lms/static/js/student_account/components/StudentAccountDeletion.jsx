/* globals gettext */
/* eslint-disable react/no-danger, import/prefer-default-export */
import React from 'react';
import PropTypes from 'prop-types';
import { Button, Icon, StatusAlert } from '@edx/paragon/static';
import StringUtils from 'edx-ui-toolkit/js/utils/string-utils';
import StudentAccountDeletionModal from './StudentAccountDeletionModal';

export class StudentAccountDeletion extends React.Component {
  constructor(props) {
    super(props);
    this.closeDeletionModal = this.closeDeletionModal.bind(this);
    this.loadDeletionModal = this.loadDeletionModal.bind(this);
    this.state = {
      deletionModalOpen: false,
      isActive: props.isActive,
      socialAuthConnected: this.getConnectedSocialAuth(),
    };
  }

  getConnectedSocialAuth() {
    const { socialAccountLinks } = this.props;
    if (socialAccountLinks && socialAccountLinks.providers) {
      return socialAccountLinks.providers.reduce((acc, value) => acc || value.connected, false);
    }

    return false;
  }

  closeDeletionModal() {
    this.setState({ deletionModalOpen: false });
    this.modalTrigger.focus();
  }

  loadDeletionModal() {
    this.setState({ deletionModalOpen: true });
  }

  render() {
    const { deletionModalOpen, socialAuthConnected, isActive } = this.state;
    const loseAccessText = StringUtils.interpolate(
      gettext('You may also lose access to verified certificates and other program credentials. If you want to make a copy of these for your records before proceeding with deletion, please go to {htmlStart}Dashboard{htmlEnd} to view your certificates.'),
      {
        htmlStart: '<a href="/dashboard" target="_blank">',
        htmlEnd: '</a>',
      },
    );

    const showError = socialAuthConnected || !isActive;

    const socialAuthError = StringUtils.interpolate(
      gettext('Before proceeding, please {htmlStart}unlink all social media accounts{htmlEnd}.'),
      {
        htmlStart: '',
        htmlEnd: '',
      },
    );

    const activationError = StringUtils.interpolate(
      gettext('Before proceeding, please {htmlStart}activate your account{htmlEnd}.'),
      {
        htmlStart: '',
        htmlEnd: '',
      },
    );

    const changeAcctInfoText = StringUtils.interpolate(
      gettext('{htmlStart}Want to change your email, name, or password instead?{htmlEnd}'),
      {
        htmlStart: '<a href="/manual" target="_blank">',
        htmlEnd: '</a>',
      },
    );

    const acctDeletionWarningText = StringUtils.interpolate(
      gettext('{strongStart}Warning: Account deletion is permanent.{strongEnd} Please read the above carefully before proceeding. This is an irreversible action, and {strongStart}you will no longer be able to use the same email on Elite A.I. Academy.{strongEnd}'),
      {
        strongStart: '<strong>',
        strongEnd: '</strong>',
      },
    );

    return (
      <div className="account-deletion-details">
        <p className="account-settings-header-subtitle">{ gettext('We’re sorry to see you go!') }</p>
        <p className="account-settings-header-subtitle">{ gettext('Please note: Deletion of your account and personal data is permanent and cannot be undone. Elite A.I. Academy will not be able to recover your account or the data that is deleted.') }</p>
        {
          // <p className="account-settings-header-subtitle">{ gettext('Once your account is deleted, you cannot use it to take courses on the edX app, edx.org, or any other site hosted by edX. This includes access to edx.org from your employer’s or university’s system and access to private sites offered by MIT Open Learning, Wharton Executive Education, and Harvard Medical School.') }</p>
        }
        <p className="account-settings-header-subtitle">{ gettext('Once your account is deleted, you cannot use it to take courses on the site hosted by Elite A.I. Academy.') }</p>
        <p
          className="account-settings-header-subtitle"
          dangerouslySetInnerHTML={{ __html: loseAccessText }}
        />
        <p
          className="account-settings-header-subtitle-warning"
          dangerouslySetInnerHTML={{ __html: acctDeletionWarningText }}
        />
        <p
          className="account-settings-header-subtitle"
          dangerouslySetInnerHTML={{ __html: changeAcctInfoText }}
        />
        <Button
          id="delete-account-btn"
          className={['btn-outline-primary']}
          disabled={showError}
          label={gettext('Delete My Account')}
          inputRef={(input) => { this.modalTrigger = input; }}
          onClick={this.loadDeletionModal}
        />
        {showError &&
          <StatusAlert
            dialog={(
              <div className="modal-alert">
                <div className="icon-wrapper">
                  <Icon id="delete-confirmation-body-error-icon" className={['fa', 'fa-exclamation-circle']} />
                </div>
                <div className="alert-content">
                  {socialAuthConnected && isActive &&
                    <p dangerouslySetInnerHTML={{ __html: socialAuthError }} />
                  }
                  {!isActive && <p dangerouslySetInnerHTML={{ __html: activationError }} /> }
                </div>
              </div>
            )}
            alertType="danger"
            dismissible={false}
            open
          />
        }
        {deletionModalOpen && <StudentAccountDeletionModal onClose={this.closeDeletionModal} />}
      </div>
    );
  }
}

StudentAccountDeletion.propTypes = {
  isActive: PropTypes.bool.isRequired,
  socialAccountLinks: PropTypes.shape({
    providers: PropTypes.arrayOf(PropTypes.object),
  }).isRequired,
};
